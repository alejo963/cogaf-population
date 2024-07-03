import torch
from torch import nn, Tensor


COGN_FUNC = ["Attention",
             "Memory",
             "Percpetion",
             "CognitiveFlexibility",
             "InhibitoryControl",
             "Language",
             "Praxia",
             "WorkingMemory",
             ]


def train_step(model: nn.Module, X_train: Tensor, y_train: Tensor, loss_fn: nn.Module, optimizer):

    model.train()

    y_logits = model(X_train).squeeze()

    loss = loss_fn(y_logits, y_train)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()


def test_step(model: nn.Module, X_test: Tensor, y_test: Tensor, loss_fn: nn.Module):

    model.eval()
    with torch.inference_mode():
        test_logits = model(X_test).squeeze()

        test_loss = loss_fn(test_logits, y_test)
        return test_loss


def train(model: nn.Module,
          X_train: Tensor,
          X_test: Tensor,
          y_train: Tensor,
          y_test: Tensor,
          loss_fn: nn.Module,
          optimizer_class,
          epochs: int,
          lr: float,
          device: torch.device = "cpu"):

    optimizer = optimizer_class(model.parameters(), lr)

    model.to(device)
    X_train, X_test = X_train.to(device), X_test.to(device)
    y_train, y_test = y_train.to(device), y_test.to(device)
    for epoch in range(epochs):
        train_loss = train_step(model, X_train, y_train, loss_fn, optimizer)
        test_loss = test_step(model, X_test, y_test, loss_fn)
        # print(
        #     f"Epoch: {epoch} | Train Loss: {train_loss:.5f} | Test loss: {test_loss:.5f}")
