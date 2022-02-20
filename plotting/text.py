#!/usr/bin/env python3
import matplotlib.pyplot as plt

def plot(x, y, text):
    plt.text(x, y, text, ha='left', va='top', transform=plt.gca().transAxes)
