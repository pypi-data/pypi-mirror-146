from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    """TextCNN

    Args:
        num_embeddings (int):
        embedding_dim (int):
        pretrained_embedding (Optional[torch.Tensor]):
        conv_kernel_sizes (list[int]):
        conv_out_channels (int):
        dropout_p (float):
        cls_hidden_size (int):
        cls_num_classes (int):
        freeze_pretrained_embeddings (bool):
    """

    def __init__(
        self,
        # embeddings
        num_embeddings: int,
        embedding_dim: int,
        pretrained_embedding: Optional[torch.Tensor],
        # convs
        conv_kernel_sizes: list[int],
        conv_out_channels: int = 128,
        # dropout
        dropout_p: float = 0.5,
        # classifier
        cls_hidden_size: int = 256,
        cls_num_classes: int = 1,
        #
        freeze_pretrained_embeddings: bool = False,
    ) -> None:
        super(TextCNN, self).__init__()

        # embeddings
        self.embedding = nn.Embedding(num_embeddings=num_embeddings, embedding_dim=embedding_dim)

        # load pretrained embeddings if provided
        if pretrained_embedding is not None:
            self.embedding.from_pretrained(
                pretrained_embedding, freeze=freeze_pretrained_embeddings
            )

        # convs
        self.convs = nn.ModuleList(
            [
                nn.Conv2d(
                    in_channels=1,
                    out_channels=conv_out_channels,
                    kernel_size=(kernel_size, embedding_dim),
                )
                for kernel_size in conv_kernel_sizes
            ]
        )

        # dropout
        self.dropout = nn.Dropout(dropout_p)

        # classifier
        self.classifier = nn.Sequential(
            nn.Linear(conv_out_channels * len(conv_kernel_sizes), cls_hidden_size),
            nn.ReLU(),
            nn.Linear(cls_hidden_size, cls_num_classes),
        )

    def forward(self, x: torch.LongTensor) -> torch.FloatTensor:
        """TODO

        Args:
            x (torch.LongTensor): TODO

        Returns:
            y_logits (torch.FloatTensor): TODO

        """
        # embeddings
        z_emb = self.embedding(x)  # shape(batch_size, max_length, embedding_dim)
        # (batch_size, in_channels=1, max_length, embedding_dim)
        z_emb_unsqueezed = z_emb.unsqueeze(1)  # add depth channel

        # convs
        # shape[(bs, out_channels, max_length - kernel_size + 1)]
        z_convs = [conv(z_emb_unsqueezed).squeeze() for conv in self.convs]

        # pooling
        # shape[(bs, out_channels, 1)]
        z_pooled = [F.max_pool1d(z_conv, z_conv.shape[2]) for z_conv in z_convs]

        # shape(bs, out_channels * len(kernel_sizes))
        z_cat = torch.cat(z_pooled, dim=1).squeeze(-1)

        # dropout
        z_dropout = self.dropout(z_cat)

        # classifier
        y_logits = self.classifier(z_dropout)

        return y_logits
