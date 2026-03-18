import matplotlib.pyplot as plt
import streamlit as st

def show_accuracy():

    epochs = [1,2,3,4,5]

    train_acc = [70,78,85,90,95]
    val_acc = [68,75,82,88,92]

    fig, ax = plt.subplots()

    ax.plot(epochs, train_acc, label="Training Accuracy")
    ax.plot(epochs, val_acc, label="Validation Accuracy")

    ax.set_xlabel("Epochs")
    ax.set_ylabel("Accuracy (%)")

    ax.set_title("Model Training Accuracy")

    ax.legend()

    st.pyplot(fig)
    