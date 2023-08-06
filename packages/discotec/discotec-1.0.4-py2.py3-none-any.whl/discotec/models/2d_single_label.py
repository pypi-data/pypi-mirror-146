import torch
import torchmetrics
import pytorch_lightning as pl
from torch import nn


__all__ = ["2DSingleLabel"]
# TODO: add mask character to something global
MASK_CHARACTER = -1


class ConvBlock(pl.LightningModule):
    def __init__(self, in_channels, out_channels, kernel_size):
        super(ConvBlock, self).__init__()

        if kernel_size % 2 == 1:
            pad_width = (kernel_size - 1) // 2
        else:
            pad_width = kernel_size // 2

        self.conv1 = nn.Conv2d(in_channels,
                               out_channels,
                               kernel_size=kernel_size,
                               padding=pad_width)

        self.conv2 = nn.Conv2d(in_channels,
                               out_channels,
                               kernel_size=kernel_size,
                               padding=pad_width)

    def forward(self, x):
        x = nn.ReLU(self.conv1(x))
        x = nn.ReLU(self.conv2(x))
        return x


class CNN2D(pl.LightningModule):
    def __init__(self,
                 in_channels,
                 learning_rate,
                 mel,
                 apply_log,
                 n_fft,
                 vertical_trim,
                 train_files,
                 val_files):
        super(CNN2D, self).__init__()
        self.in_channels = in_channels
        self.kernel_size = 3
        self._setup_layers()
        self.accuracy = torchmetrics.Accuracy()
        self.learning_rate = learning_rate
        self.mel = mel
        self.apply_log = apply_log
        self.n_fft = n_fft
        self.vertical_trim = vertical_trim
        self.train_files = list(train_files)
        self.val_files = list(val_files)
        self.save_hyperparameters()

    def _setup_layers(self):
        base = 2
        self.conv1 = ConvBlock(in_channels=self.in_channels, out_channels=base**5, kernel_size=self.kernel_size)
        self.conv2 = ConvBlock(in_channels=base**5, out_channels=base**6, kernel_size=self.kernel_size)
        self.conv3 = ConvBlock(in_channels=base**6, out_channels=base**7, kernel_size=self.kernel_size)
        self.conv4 = ConvBlock(in_channels=base**7, out_channels=base**8, kernel_size=self.kernel_size)
        self.conv9 = ConvBlock(in_channels=base**8, out_channels=base**8, kernel_size=self.kernel_size)
        self.conv5 = ConvBlock(in_channels=base**8, out_channels=base**7, kernel_size=self.kernel_size)
        self.conv6 = ConvBlock(in_channels=base**7, out_channels=base**6, kernel_size=self.kernel_size)
        self.conv7 = ConvBlock(in_channels=base**6, out_channels=base**5, kernel_size=self.kernel_size)
        self.conv8 = ConvBlock(in_channels=base**5, out_channels=base**5, kernel_size=self.kernel_size)

        self.conv_out = nn.Conv2d(in_channels=base**5, out_channels=3, kernel_size=(3, 3))

    def _forward(self, x):
        x = nn.ReLU(self.conv1(x))
        x = nn.ReLU(self.conv2(x))
        x = nn.ReLU(self.conv3(x))
        x = nn.ReLU(self.conv4(x))
        x = nn.ReLU(self.conv5(x))
        x = nn.ReLU(self.conv6(x))
        x = nn.ReLU(self.conv7(x))
        x = nn.ReLU(self.conv8(x))
        x = nn.ReLU(self.conv9(x))
        return x

    def _shared_step(self, batch):

        if len(batch) == 3:
            x, x_mask, y = batch
            logits = self.forward(x, x_mask)
        else:
            x, y = batch
            logits = self.forward(x)

        loss = torch.nn.functional.nll_loss(logits, y, ignore_index=self.mask_character)
        preds = logits.argmax(dim=1)
        preds = preds[y != self.mask_character]
        labels = y[y != self.mask_character]
        acc = self.accuracy(preds, labels)
        return loss, acc

    def training_step(self, batch, batch_nb):
        loss, acc = self._shared_step(batch)
        return {"loss": loss, "train_acc": acc}

    def validation_step(self, batch, batch_nb):
        loss, acc = self._shared_step(batch)
        return {"val_loss": loss, "val_acc": acc}

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return {
            "optimizer": optimizer,
            "lr_scheduler": torch.optim.lr_scheduler.StepLR(
                optimizer, step_size=150, gamma=0.7
            ),
        }

    def training_epoch_end(self, outputs):
        train_loss = self.all_gather([x["loss"] for x in outputs])
        train_acc = self.all_gather([x["train_acc"] for x in outputs])
        loss = torch.mean(torch.stack(train_loss))
        acc = torch.mean(torch.stack(train_acc))
        self.log("train_loss", loss)
        self.log("train_acc", acc)
        self.log("learning_rate", self.learning_rate)

    def on_train_start(self):
        self.log("hp_metric", self.learning_rate + self.n_fft)

    def validation_epoch_end(self, outputs):
        val_loss = self.all_gather([x["val_loss"] for x in outputs])
        val_acc = self.all_gather([x["val_acc"] for x in outputs])
        val_loss = torch.mean(torch.stack(val_loss))
        val_acc = torch.mean(torch.stack(val_acc))
        self.log("val_loss", val_loss)
        self.log("val_acc", val_acc)
