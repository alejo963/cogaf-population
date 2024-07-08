import torch
from torch import nn, Tensor
from pathlib import Path
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.exceptions import UndefinedMetricWarning

import warnings
warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


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

    return loss


def test_step(model: nn.Module, X_test: Tensor, y_test: Tensor, loss_fn: nn.Module):

    model.eval()
    with torch.inference_mode():
        test_logits = model(X_test).squeeze()

        test_loss = loss_fn(test_logits, y_test)
        test_pred = test_logits.argmax(dim=1).to("cpu")
        get_metrics(test_pred, y_test.cpu())
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
          device: torch.device = "cpu",
          verbose: bool = False):

    optimizer = optimizer_class(model.parameters(), lr)

    model.to(device)
    X_train, X_test = X_train.to(device), X_test.to(device)
    y_train, y_test = y_train.to(device), y_test.to(device)
    for epoch in range(epochs):
        train_loss = train_step(model, X_train, y_train, loss_fn, optimizer)
        if verbose:
            if epoch % 100 == 0:
                print(f"Epoch: {epoch}")
                test_loss = test_step(model, X_test, y_test, loss_fn)
                print(
                    f"Train Loss: {train_loss} | Test loss: {test_loss}")

                print("---------------------------------------------------------")


def save_model(model, name):

    # Create models directory (if it doesn't already exist), see: https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
    MODEL_PATH = Path("models")
    MODEL_PATH.mkdir(parents=True,  # create parent directories if needed
                     exist_ok=True  # if models directory already exists, don't error
                     )

    # Create model save path
    MODEL_SAVE_PATH = MODEL_PATH / name

    # Save the model state dict
    print(f"Saving model to: {MODEL_SAVE_PATH}")
    torch.save(obj=model.state_dict(),  # only saving the state_dict() only saves the learned parameters
               f=MODEL_SAVE_PATH)


def get_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro")
    prec = precision_score(y_true, y_pred, average="macro")
    recall = recall_score(y_true, y_pred, average="macro")

    print("Accuracy: ", acc, " | F1-score: ", f1,
          " | Precision: ", prec, " | Recall: ", recall)

    return (acc, f1, prec, recall)
