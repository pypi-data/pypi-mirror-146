import torch
import torch_multilabel_embedding as tml


def cossim(a, b, tol=1e-8):
    """ Cosine similarity with normalized input vectors """
    # normalize
    a = torch.nn.functional.normalize(a, p=2, dim=1)
    b = torch.nn.functional.normalize(b, p=2, dim=1)
    # compute cosine simi.
    n = torch.sum(torch.mul(a, b), dim=1)
    da = torch.sqrt(torch.sum(torch.pow(a, 2), dim=1))
    db = torch.sqrt(torch.sum(torch.pow(b, 2), dim=1))
    return n / torch.maximum(da * db, torch.tensor(tol))


class SimiLoss(torch.nn.Module):
    def __init__(self,
                 embedding: torch.Tensor = None,
                 tokenlist_size: int = None,
                 embedding_size: int = None,
                 context_weights: torch.Tensor = None,
                 context_size: int = None,
                 context_trainable: bool = False,
                 random_state: int = None):
        """ Train an input multi-label embedding as a similarity learning
              problem

        Parameters:
        -----------
        embedding : torch.Tensor (Default: None)
            A pretrained embedding with the dimension
              <tokenlist_size, embedding_size>

        tokenlist_size : int (Default: None)
            The size of the token list, and thus, the number of embedding
              vectors. If `embedding=None`, specify tokenlist_size.

        embedding_size : int (Default: None)
            The embedding dimension, or resp., the output vector dimension.
              If `embedding=None`, specify embedding_size.

        context_weights : torch.Tensor (Default: None)
            A predefined weighting scheme to average the context vectors.
            The `len(context_weights)` must correspond to the training data.

        context_size : int (Default: None)
            If context_weights=None, specify `context_size`. An equal-weighting
              scheme will be initialized.

        context_trainable : bool (Default: False)
            If the context weights are trainable, then the softmax function is
              applied on the context weights `softmax(context_weights)` to
              ensure `sum(context_weights)=1`.
        """
        super(SimiLoss, self).__init__()

        # store embedding size
        if embedding is None:
            self.tokenlist_size = tokenlist_size  # v
            self.embedding_size = embedding_size  # e
        else:
            self.tokenlist_size, self.embedding_size = embedding.shape

        # init embedding layer
        self.emb = tml.MultiLabelEmbedding(
            vocab_size=self.tokenlist_size,
            embed_size=self.embedding_size,
            random_state=random_state)

        # set pretrained embedding weights
        if embedding is None:
            # Normal distribution N(mu=0, sig=0.274..)
            torch.nn.init.normal_(
                self.emb.weight, mean=0.0, std=0.2745960056781769)
        else:
            self.emb.weight.data = embedding

        # store params for context scheme
        if context_weights is None:
            self.context_size = context_size  # m
        else:
            self.context_size = context_weights.shape[0]

        # init context weights
        self.context_weights = torch.nn.parameter.Parameter(
            torch.empty(self.context_size))

        if context_weights is None:
            # equal-weighted context vectors
            torch.nn.init.constant_(
                self.context_weights, 1.0 / self.context_size)
        else:
            self.context_weights.weight.data = context_weights

        # are the context weights trainable?
        self.context_trainable = context_trainable
        self.context_weights.requires_grad = self.context_trainable

    def get_indices(self, max_idx: int):
        # precompute indicies
        trgt_idx = self.context_size // 2
        ctx_idx = list(range(self.context_size + 1))
        ctx_idx.remove(trgt_idx)
        # add range indicies
        indices = torch.arange(max_idx)
        ctx_idx = indices.repeat(self.context_size, 1).t() \
            + torch.tensor(ctx_idx).repeat(max_idx, 1)
        trgt_idx = indices + torch.tensor(trgt_idx)
        return trgt_idx, ctx_idx

    def trainable_embedding(self, trainable):
        for param in self.emb.parameters():
            param.requires_grad = trainable

    def _get_context(self):
        if self.context_trainable:
            return torch.nn.functional.softmax(
                self.context_weights, dim=0)
        else:
            return self.context_weights

    def _similarity_score(self, b, C):
        """
        Parameters:
        -----------
        b : torch.tensor[batch_sz, embed_sz]
          The target vector

        C : torch.tensor[batch_sz, context_sz, embed_sz]
          Context vectors (Basically the features `X` to predict `y`)
        """
        # apply (trained) weighting scheme to context emb. vectors
        h = self._get_context()
        h = torch.matmul(h, C)
        # compute similarity score
        f = cossim(b, h)
        return f

    def forward(self, b, C, nb, nC):
        b = self.emb(b)
        C = self.emb(C)
        nb = self.emb(nb)
        nC = self.emb(nC)

        # similarity functions
        po = self._similarity_score(b, C)
        n1 = self._similarity_score(nb, C)
        n2 = self._similarity_score(b, nC)

        # contrastive loss function
        loss = (-po + .5 * n1 + .5 * n2).mean()

        # done
        return loss
