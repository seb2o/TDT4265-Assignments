import numpy as np
import utils


class BaseTrainer:

    def __init__(
            self,
            model,
            learning_rate: float,
            batch_size: int,
            shuffle_dataset: bool,
            X_train: np.ndarray, Y_train: np.ndarray,
            X_val: np.ndarray, Y_val: np.ndarray, ) -> None:
        """
            Initialize the trainer responsible for performing the gradient descent loop.
        """
        self.X_train = X_train
        self.Y_train = Y_train
        self.X_val = X_val
        self.Y_val = Y_val
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.model = model
        self.shuffle_dataset = shuffle_dataset

    def validation_step(self):
        """
        Perform a validation step to evaluate the model at the current step for the validation set.
        Also calculates the current accuracy of the model on the train set.
        Returns:
            loss (float): cross entropy loss over the whole dataset
            accuracy_ (float): accuracy over the whole dataset
        Returns:
            loss value (float) on batch
            accuracy_train (float): Accuracy on train dataset
            accuracy_val (float): Accuracy on the validation dataset
        """
        pass

    def train_step(self, X, Y):
        """
            Perform forward, backward and gradient descent step here.
        Args:
            X: one batch of images
            Y: one batch of labels
        Returns:
            loss value (float) on batch
        """
        pass

    def train(
            self,
            num_epochs: int):
        """
        Training loop for model.
        Implements stochastic gradient descent with num_epochs passes over the train dataset.
        Returns:
            train_history: a dictionary containing loss and accuracy over all training steps
            val_history: a dictionary containing loss and accuracy over a selected set of steps
        """
        # Utility variables
        num_batches_per_epoch = self.X_train.shape[0] // self.batch_size
        num_steps_per_val = num_batches_per_epoch // 5
        # A tracking value of loss over all training steps
        train_history = dict(
            loss={},
            accuracy={}
        )
        val_history = dict(
            loss={},
            accuracy={}
        )

        global_step = 0
        for epoch in range(num_epochs):
            train_loader = utils.batch_loader(
                self.X_train, self.Y_train, self.batch_size, shuffle=self.shuffle_dataset)
            for X_batch, Y_batch in iter(train_loader):
                loss = self.train_step(X_batch, Y_batch)
                # Track training loss continuously
                train_history["loss"][global_step] = loss

                # Track validation loss / accuracy every time we progress 20% through the dataset
                if global_step % num_steps_per_val == 0:
                    val_loss, accuracy_train, accuracy_val = self.validation_step()
                    train_history["accuracy"][global_step] = accuracy_train
                    val_history["loss"][global_step] = val_loss
                    val_history["accuracy"][global_step] = accuracy_val
                    if early_stopping_check(val_history["loss"], global_step, num_steps_per_val):
                        print(f"Stopped training at step {global_step + 1} due to validation not improving anymore ")
                        return train_history, val_history
                global_step += 1
        return train_history, val_history

    # helper function for early stopping
    # go trough the list


def early_stopping_check(loss_history, current_step, num_step_per_val, patience=10):
    check_limit = (patience-1)*num_step_per_val
    if current_step < check_limit:
        return False
    current_loss = loss_history[current_step]
    for step in range(current_step, current_step - check_limit, -num_step_per_val):
        previous_loss = loss_history[step - num_step_per_val]
        if current_loss < previous_loss:
            return False
        current_loss = previous_loss
    return True
