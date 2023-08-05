import torch
import torch.nn as nn
import torch.nn.functional as F


class HierarchicalPool(nn.Module):
    def __init__(self) -> None:
        super(HierarchicalPool, self).__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x


class SWEM(nn.Module):
    r"""Simple Word Embedding Model

    [paper](https://arxiv.org/pdf/1805.09843.pdf)
    [code](https://github.com/dinghanshen/SWEM/)

    Attributes:
    """

    def __init__(
        self,
        num_embeddings: int,
        embedding_dim: int,
        hidden_dim: int,
        pooling: str,
        out_features: int,
        pretraiend_embeddings: torch.Tensor | None = None,
    ) -> None:
        super(SWEM, self).__init__()

        # embedding layer
        self.embedding = nn.Embedding(num_embeddings, embedding_dim)

        if pretraiend_embeddings:
            self.embedding.from_pretrained(pretraiend_embeddings)

        # pre-pooling
        self.nonlinear1 = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

        # pooling
        self.pooling: str = pooling

        # post-pooling
        if self.pooling == "cat":
            hidden_dim *= 2

        self.nonlinear2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_features),
        )

    def forward(self, x_input: torch.Tensor) -> torch.Tensor:
        # x_input: shape(bs, max_length)

        # embedding
        x_emb = self.embedding(x_input)  # shape(bs, max_length, embedding_dim)

        # pre-pooling
        x_nonlinear1 = self.nonlinear1(x_emb)  # shape(bs, max_length, hidden_dim)

        # pooling
        x_pools = []

        if self.pooling in {"max", "cat"}:
            x_pools.append(F.max_pool2d(x_nonlinear1, kernel_size=(x_nonlinear1.shape[1], 1)))

        if self.pooling in {"avg", "cat"}:
            x_pools.append(F.avg_pool2d(x_nonlinear1, kernel_size=(x_nonlinear1.shape[1], 1)))

        if self.pooling in {"hier"}:
            # TODO
            pass

        x_pool = torch.cat(x_pools, dim=-1)
        x_pool = x_pool.squeeze()  # shape(bs, hidden_dim)

        # post-pooling
        x_nonlinear2 = self.nonlinear2(x_pool)  # shape(bs, out_features)

        return x_nonlinear2
