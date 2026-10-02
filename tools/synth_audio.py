#!/usr/bin/env python3
"""
Still Water - procedural audio.  No samples, no external assets: every sound is synthesised here (numpy/scipy) and written
as OGG Vorbis into assets/audio/{sfx,amb,music}.  Deterministic (seeded).

    /opt/tools/venv/bin/python tools/synth_audio.py [name ...]
"""
import os, sys, math
import numpy as np
from scipy import signal
import soundfile as sf

SR = 22050
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "audio")
RNG = np.random.default_rng(7)

# ------------------------------------------------------------------ primitives
class Sig(np.ndarray):
    """1-D signal that pads the shorter operand with silence, so layers of different lengths can simply be added or multiplied"""
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if "out" in kwargs:
            kwargs["out"] = tuple(np.asarray(o) if isinstance(o, np.ndarray) else o for o in kwargs["out"])
        if method == "__call__" and len(inputs) == 2 and all(isinstance(i, np.ndarray) and i.ndim == 1 for i in inputs) \
                and len(inputs[0]) != len(inputs[1]):
            n = max(len(inputs[0]), len(inputs[1]))
            a = np.pad(np.asarray(inputs[0]), (0, n - len(inputs[0])))
            b = np.pad(np.asarray(inputs[1]), (0, n - len(inputs[1])))
            return ufunc(a, b, **kwargs).view(Sig)
        inputs = [np.asarray(i) if isinstance(i, Sig) else i for i in inputs]
        out = getattr(ufunc, method)(*inputs, **kwargs)
        return out.view(Sig) if isinstance(out, np.ndarray) and out.ndim == 1 else out

def S(x):
    return np.asarray(x).view(Sig)

def N(sec):
    return int(sec * SR)

def t_(sec):
    return np.arange(N(sec)) / SR

def noise(sec):
    return S(RNG.standard_normal(N(sec)))

def sine(f, sec, ph=0.0):
    return S(np.sin(2 * np.pi * f * t_(sec) + ph))

def lp(x, fc, order=2):
    return S(signal.sosfilt(signal.butter(order, min(fc, SR / 2 - 100) / (SR / 2), "low", output="sos"), np.asarray(x)))

def hp(x, fc, order=2):
    return S(signal.sosfilt(signal.butter(order, fc / (SR / 2), "high", output="sos"), np.asarray(x)))

def bp(x, lo, hi, order=2):
    return S(signal.sosfilt(signal.butter(order, [lo / (SR / 2), min(hi, SR / 2 - 100) / (SR / 2)], "band", output="sos"), np.asarray(x)))

def pink(sec):
    x = noise(sec)
    return lp(x, 900) * 2.0 + lp(x, 120) * 4.0

def env(sec, a=0.003, d=0.2, floor=0.0):
    """attack then exponential decay; d = time constant in seconds"""
    t = t_(sec)
    e = np.exp(-t / max(d, 1e-4))
    e = np.where(t < a, t / a, e)
    return S(e)

def adsr(sec, a=0.01, dec=0.1, sus=0.6, rel=0.2):
    n = N(sec)
    e = np.ones(n) * sus
    na, nd, nr = N(a), N(dec), N(rel)
    e[:na] = np.linspace(0, 1, max(na, 1))
    e[na:na + nd] = np.linspace(1, sus, max(nd, 1))[: max(0, n - na)][: len(e[na:na + nd])]
    if nr > 0:
        e[-nr:] *= np.linspace(1, 0, nr)
    return S(e)

def bell(f, sec, d=0.6, parts=((1, 1.0), (2.76, 0.5), (5.4, 0.25), (8.9, 0.1)), a=0.002):
    x = S(np.zeros(N(sec)))
    for k, g in parts:
        x += g * np.sin(2 * np.pi * f * k * t_(sec)) * env(sec, a, d / (0.6 + 0.4 * k))
    return x

def pluck(f, sec, d=0.35):
    return (sine(f, sec) + 0.4 * sine(f * 2, sec) + 0.15 * sine(f * 3, sec)) * env(sec, 0.002, d)

def sweep(f0, f1, sec, shape="exp"):
    t = t_(sec)
    if shape == "exp":
        f = f0 * (f1 / f0) ** (t / sec)
    else:
        f = f0 + (f1 - f0) * t / sec
    return S(np.sin(2 * np.pi * np.cumsum(f) / SR))

def saw(f, sec):
    return S(signal.sawtooth(2 * np.pi * f * t_(sec)))

def click(sec=0.02, fc=2500, d=0.004):
    return lp(noise(sec), fc) * env(sec, 0.0005, d)

def fit(x, sec):
    n = N(sec)
    return S(np.pad(np.asarray(x), (0, max(0, n - len(x))))[:n])

def at(canvas, x, t0, gain=1.0):
    i = N(t0)
    n = min(len(x), len(canvas) - i)
    if n > 0:
        canvas[i:i + n] += x[:n] * gain
    return canvas

def canvas(sec):
    return S(np.zeros(N(sec)))

def reverb(x, wet=0.25, tail=1.3, damp=3500):
    n = N(tail)
    ir = noise(tail) * np.exp(-t_(tail) / (tail / 5.0))
    ir = lp(ir, damp)
    ir[0] = 0
    y = signal.fftconvolve(x, ir)
    y = y / (np.max(np.abs(y)) + 1e-9) * np.max(np.abs(x))
    out = np.pad(x, (0, len(y) - len(x))) * (1 - wet) + y * wet
    return S(out)

def fade(x, a=0.004, b=0.01):
    x = x.copy()
    na, nb = N(a), N(b)
    if na:
        x[:na] *= np.linspace(0, 1, na)
    if nb:
        x[-nb:] *= np.linspace(1, 0, nb)
    return x

def norm(x, peak=0.85):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak

def loopify(x, xf=1.2):
    """make a seamless loop: overlap the tail onto the head"""
    n = N(xf)
    head, tail = x[:n].copy(), x[-n:].copy()
    w = np.linspace(0, 1, n)
    body = x[:-n].copy()
    body[:n] = head * w + tail * (1 - w)
    return body

# ------------------------------------------------------------------- SFX
SFX = {}
def sfx(fn):
    SFX[fn.__name__.lstrip("_")] = fn
    return fn

@sfx
def tap():
    return norm(click(0.05, 1800, 0.01) + 0.5 * sine(620, 0.05) * env(0.05, 0.001, 0.012), 0.6)

@sfx
def take():
    c = canvas(0.35)
    at(c, pluck(660, 0.3, 0.12), 0.0)
    at(c, pluck(990, 0.3, 0.14), 0.07, 0.8)
    at(c, click(0.03, 3000), 0.0, 0.4)
    return norm(c, 0.65)

@sfx
def wrong():
    return norm(lp(noise(0.18), 500) * env(0.18, 0.002, 0.05) + sweep(150, 90, 0.18) * env(0.18, 0.002, 0.07), 0.6)

@sfx
def solve():
    c = canvas(1.4)
    for k, f in enumerate((784, 988, 1175)):
        at(c, bell(f, 1.2, 0.45), 0.09 * k, 0.8)
    return norm(reverb(c, 0.3, 0.8), 0.7)

@sfx
def turn():
    return norm(bp(noise(0.35), 150, 900) * adsr(0.35, 0.1, 0.1, 0.5, 0.18), 0.4)

@sfx
def back():
    return norm(bp(noise(0.25), 200, 1200) * adsr(0.25, 0.04, 0.1, 0.4, 0.14), 0.35)

@sfx
def rustle():
    x = bp(noise(0.5), 1800, 7000) * (0.5 + 0.5 * np.abs(sine(11, 0.5)))
    return norm(x * adsr(0.5, 0.03, 0.2, 0.6, 0.2), 0.5)

@sfx
def locked():
    c = canvas(0.4)
    for k in range(3):
        at(c, click(0.03, 1500, 0.008) + 0.4 * sine(300, 0.03) * env(0.03, 0.001, 0.01), 0.1 * k)
    return norm(c, 0.6)

@sfx
def unlock():
    c = canvas(0.5)
    at(c, click(0.03, 3500, 0.006), 0.0)
    at(c, 0.7 * sine(180, 0.3) * env(0.3, 0.002, 0.07) + lp(noise(0.3), 700) * env(0.3, 0.002, 0.04), 0.12)
    return norm(c, 0.75)

@sfx
def hollow():
    x = sweep(240, 160, 0.4) * env(0.4, 0.001, 0.09) + 0.3 * lp(noise(0.4), 800) * env(0.4, 0.001, 0.02)
    return norm(x, 0.75)

@sfx
def dial():
    return norm(click(0.04, 3000, 0.006) + 0.4 * sine(1800, 0.04) * env(0.04, 0.0005, 0.006), 0.6)

@sfx
def tick():
    return norm(click(0.03, 4000, 0.004) + 0.5 * sine(1500, 0.03) * env(0.03, 0.0005, 0.005), 0.55)

@sfx
def book():
    return norm(bp(noise(0.4), 300, 2500) * adsr(0.4, 0.05, 0.2, 0.7, 0.15) + 0.4 * fit(lp(noise(0.1), 400) * env(0.1, 0.002, 0.03), 0.4), 0.5)

@sfx
def match():
    c = canvas(1.0)
    at(c, bp(noise(0.12), 800, 6000) * env(0.12, 0.002, 0.05), 0.0, 0.8)
    at(c, hp(noise(0.8), 3000) * adsr(0.8, 0.1, 0.3, 0.3, 0.4), 0.05, 0.4)
    return norm(c, 0.6)

@sfx
def flame():
    return norm(lp(noise(1.0), 1800) * adsr(1.0, 0.25, 0.3, 0.4, 0.4) + 0.2 * sine(90, 1.0) * adsr(1.0, 0.2, 0.2, 0.4, 0.4), 0.55)

@sfx
def flame_back():
    x = lp(noise(1.6), 1800) * adsr(1.6, 0.25, 0.3, 0.4, 0.4)
    return norm(x[::-1], 0.55)

@sfx
def pour():
    n = N(1.0)
    glug = bp(noise(1.0), 300, 1600) * (0.6 + 0.4 * np.sin(2 * np.pi * (6 + 4 * np.linspace(0, 1, n)) * t_(1.0)))
    return norm(glug * adsr(1.0, 0.08, 0.2, 0.7, 0.3), 0.55)

@sfx
def reveal():
    return norm(reverb(lp(noise(1.0), 1200) * adsr(1.0, 0.5, 0.1, 0.5, 0.4) + 0.3 * sine(440, 1.0) * adsr(1.0, 0.5, 0.1, 0.5, 0.4), 0.3, 0.8), 0.4)

@sfx
def pell_talk():
    # pitched bubbles, one per syllable: never words
    c = canvas(0.9)
    for k, (f0, f1) in enumerate(((420, 760), (560, 940), (380, 690), (620, 1000))):
        at(c, sweep(f0, f1, 0.09) * env(0.09, 0.004, 0.03), 0.17 * k, 0.8)
    return norm(c, 0.55)

@sfx
def pell_eat():
    c = canvas(0.8)
    for k in range(4):
        at(c, sweep(300, 180, 0.07) * env(0.07, 0.003, 0.025), 0.14 * k)
    at(c, sweep(500, 950, 0.1) * env(0.1, 0.003, 0.04), 0.62, 0.6)
    return norm(c, 0.55)

@sfx
def jar_open():
    c = canvas(0.6)
    at(c, sweep(500, 800, 0.05) * env(0.05, 0.001, 0.02) + click(0.02, 2000), 0.0)
    at(c, bp(noise(0.4), 2000, 6000) * (0.5 + 0.5 * np.abs(sine(25, 0.4))) * env(0.4, 0.05, 0.2), 0.12, 0.35)
    return norm(c, 0.55)

@sfx
def flutter():
    return norm(bp(noise(0.7), 1500, 6000) * (0.5 + 0.5 * np.abs(sine(22, 0.7))) * adsr(0.7, 0.05, 0.2, 0.8, 0.25), 0.45)

@sfx
def clock_open():
    c = canvas(0.6)
    at(c, click(0.03, 3000) + 0.5 * sine(900, 0.03) * env(0.03, 0.001, 0.01), 0.0)
    at(c, bell(1400, 0.4, 0.12) * 0.3, 0.05)
    at(c, bp(noise(0.25), 300, 1500) * adsr(0.25, 0.03, 0.2, 0.5, 0.1), 0.1, 0.5)
    return norm(c, 0.6)

@sfx
def cabinet():
    t = t_(0.8)
    f = 130 + 25 * np.sin(2 * np.pi * 9 * t) + 40 * t
    x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * adsr(0.8, 0.08, 0.2, 0.5, 0.25)
    return norm(lp(x, 900) + 0.15 * bp(noise(0.8), 300, 1200) * adsr(0.8, 0.1, 0.2, 0.5, 0.2), 0.4)

@sfx
def fragment():
    c = canvas(0.8)
    at(c, bp(noise(0.3), 2000, 7000) * (0.5 + 0.5 * np.abs(sine(18, 0.3))) * env(0.3, 0.01, 0.12), 0.0, 0.5)
    at(c, bell(1319, 0.7, 0.35) * 0.7, 0.1)
    at(c, bell(1760, 0.6, 0.3) * 0.5, 0.2)
    return norm(reverb(c, 0.25, 0.7), 0.6)

@sfx
def mirror():
    c = canvas(0.9)
    at(c, bell(2093, 0.8, 0.4, parts=((1, 1), (1.5, 0.4), (2.3, 0.3))) * 0.6, 0.0)
    at(c, bell(2093 * 1.005, 0.8, 0.4, parts=((1, 1), (1.5, 0.4))) * 0.5, 0.5)
    return norm(reverb(c, 0.35, 1.0), 0.45)

@sfx
def lantern_set():
    c = canvas(0.9)
    at(c, bell(1568, 0.8, 0.4, parts=((1, 1), (2.4, 0.3))) * 0.6, 0.0)
    at(c, bell(2093, 0.7, 0.3, parts=((1, 1), (2.4, 0.3))) * 0.4, 0.08)
    return norm(reverb(c, 0.2, 0.6), 0.45)

@sfx
def crate():
    c = canvas(0.6)
    at(c, bp(noise(0.5), 150, 1800) * env(0.5, 0.004, 0.08), 0.0, 0.8)
    at(c, sweep(300, 120, 0.2) * env(0.2, 0.002, 0.05), 0.0, 0.5)
    return norm(c, 0.7)

@sfx
def heron():
    c = canvas(0.9)
    for k in range(3):
        at(c, bp(noise(0.12), 200, 1400) * env(0.12, 0.004, 0.04), 0.13 * k, 0.9 - 0.2 * k)
    at(c, bp(noise(0.5), 400, 3000) * adsr(0.5, 0.05, 0.2, 0.4, 0.3), 0.3, 0.3)
    return norm(c, 0.5)

@sfx
def cork():
    return norm(sweep(180, 90, 0.12) * env(0.12, 0.002, 0.03) + 0.4 * click(0.05, 1500, 0.01), 0.7)

@sfx
def gear_on():
    return norm(click(0.03, 3000) + bell(1800, 0.3, 0.1, parts=((1, 1), (3.1, 0.3))) * 0.5 + 0.3 * lp(noise(0.2), 900) * env(0.2, 0.002, 0.04), 0.6)

@sfx
def gear_off():
    return norm(bell(1500, 0.3, 0.09, parts=((1, 1), (3.1, 0.3))) * 0.5 + 0.3 * lp(noise(0.2), 900) * env(0.2, 0.002, 0.04), 0.5)

@sfx
def grind():
    t = t_(0.9)
    x = lp(noise(0.9), 1400) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 14 * t))) + 0.3 * saw(70, 0.9)
    return norm(lp(x, 1800) * adsr(0.9, 0.05, 0.2, 0.8, 0.3), 0.5)

@sfx
def winch():
    c = canvas(2.4)
    for k in range(10):
        at(c, click(0.04, 1800, 0.008) + 0.5 * sine(120, 0.05) * env(0.05, 0.002, 0.02), 0.22 * k, 0.8)
    at(c, lp(noise(2.4), 300) * adsr(2.4, 0.3, 0.2, 0.5, 0.6), 0.0, 0.5)
    return norm(c, 0.6)

@sfx
def oarlock():
    return norm(sweep(260, 190, 0.15) * env(0.15, 0.002, 0.05) + 0.5 * lp(noise(0.12), 1000) * env(0.12, 0.002, 0.03), 0.65)

@sfx
def pushoff():
    c = canvas(1.6)
    at(c, bp(noise(1.5), 150, 1200) * adsr(1.5, 0.1, 0.3, 0.6, 0.8), 0.0, 0.5)
    at(c, sweep(110, 70, 0.3) * env(0.3, 0.003, 0.1), 0.0, 0.5)
    return norm(c, 0.55)

@sfx
def chain():
    c = canvas(1.0)
    for k in range(9):
        at(c, bell(2200 + RNG.integers(-300, 300), 0.15, 0.04, parts=((1, 1), (2.7, 0.4))) * 0.4 + click(0.01, 4000), 0.06 * k * (1 + 0.1 * k), 0.8 - 0.07 * k)
    return norm(c, 0.55)

@sfx
def patch():
    return norm(lp(noise(0.5), 600) * adsr(0.5, 0.05, 0.2, 0.6, 0.2) + 0.2 * sweep(160, 100, 0.3), 0.5)

@sfx
def tar():
    return norm(lp(noise(0.6), 450) * adsr(0.6, 0.15, 0.2, 0.5, 0.3), 0.45)

@sfx
def bell_():
    return norm(reverb(bell(587, 2.2, 1.0, parts=((1, 1), (2.01, 0.55), (2.76, 0.4), (4.07, 0.2))), 0.25, 1.2), 0.75)
SFX["bell"] = bell_
del SFX["bell_"]

@sfx
def rope():
    t = t_(0.5)
    x = signal.sawtooth(2 * np.pi * np.cumsum(90 + 30 * np.sin(2 * np.pi * 7 * t)) / SR) * adsr(0.5, 0.05, 0.2, 0.5, 0.2)
    return norm(lp(x, 700) * 0.6 + bp(noise(0.5), 300, 1500) * 0.15, 0.4)

@sfx
def splash():
    c = canvas(0.8)
    at(c, bp(noise(0.5), 300, 5000) * env(0.5, 0.004, 0.1), 0.0, 0.9)
    for k in range(5):
        at(c, sweep(900 + 200 * k, 500, 0.06) * env(0.06, 0.002, 0.02), 0.05 + 0.08 * k, 0.3)
    return norm(c, 0.6)

@sfx
def oar():
    c = canvas(0.9)
    at(c, bp(noise(0.5), 200, 2500) * adsr(0.5, 0.15, 0.2, 0.4, 0.2), 0.0, 0.6)
    at(c, lp(noise(0.3), 700) * env(0.3, 0.01, 0.1), 0.45, 0.5)
    at(c, sweep(220, 140, 0.15) * env(0.15, 0.003, 0.05), 0.05, 0.3)
    return norm(c, 0.5)

@sfx
def oar_idle():
    return norm(bp(noise(0.6), 200, 2000) * adsr(0.6, 0.2, 0.2, 0.4, 0.2), 0.4)

@sfx
def oar_stuck():
    return norm(lp(noise(0.7), 500) * adsr(0.7, 0.05, 0.2, 0.6, 0.3) + 0.4 * sweep(110, 60, 0.7) * adsr(0.7, 0.05, 0.2, 0.5, 0.2), 0.5)

@sfx
def scrape():
    t = t_(0.9)
    x = bp(noise(0.9), 150, 1800) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t)) * adsr(0.9, 0.05, 0.2, 0.7, 0.3)
    return norm(x + 0.3 * saw(55, 0.9) * adsr(0.9, 0.05, 0.2, 0.6, 0.3), 0.55)

@sfx
def float_chime():
    return norm(reverb(bell(1047, 1.6, 0.8, parts=((1, 1), (2.76, 0.3), (5.4, 0.1))), 0.35, 1.1), 0.55)

@sfx
def buoy_long():
    return norm(reverb(bell(246, 2.2, 1.1, parts=((1, 1), (2.0, 0.5), (3.0, 0.3), (4.2, 0.15))), 0.25, 1.1), 0.7)

@sfx
def buoy_short():
    return norm(reverb(bell(246, 0.7, 0.22, parts=((1, 1), (2.0, 0.5), (3.0, 0.3), (4.2, 0.15))), 0.2, 0.7), 0.7)

@sfx
def bell_long():
    return norm(reverb(bell(494, 1.8, 0.9, parts=((1, 1), (2.01, 0.5), (2.76, 0.35), (4.1, 0.15))), 0.25, 1.0), 0.7)

@sfx
def bell_short():
    return norm(reverb(bell(494, 0.55, 0.18, parts=((1, 1), (2.01, 0.5), (2.76, 0.35), (4.1, 0.15))), 0.2, 0.6), 0.7)

@sfx
def buoy_answer():
    x = reverb(bell(185, 3.4, 1.8, parts=((1, 1), (2.0, 0.4), (3.0, 0.25))), 0.5, 2.0, 1800)
    return norm(lp(x, 2200) * 0.9, 0.6)

@sfx
def bell_far():
    x = reverb(bell(392, 3.0, 1.6, parts=((1, 1), (2.01, 0.45), (2.76, 0.3))), 0.6, 2.2, 1500)
    return norm(lp(x, 1800), 0.5)

@sfx
def compass():
    c = canvas(0.4)
    at(c, click(0.02, 3500), 0.0)
    at(c, bp(noise(0.3), 1500, 5000) * env(0.3, 0.02, 0.08), 0.02, 0.25)
    return norm(c, 0.5)

@sfx
def throw():
    return norm(bp(noise(0.5), 400, 3500) * adsr(0.5, 0.06, 0.3, 0.3, 0.2) * np.linspace(0.4, 1.0, N(0.5)) ** 2, 0.5)

@sfx
def sting():
    c = canvas(1.2)
    for f in (233, 247, 262, 277, 466, 494):
        at(c, signal.sawtooth(2 * np.pi * f * t_(1.2)) * env(1.2, 0.002, 0.45), 0.0, 0.3)
    at(c, noise(0.5) * env(0.5, 0.001, 0.12), 0.0, 0.8)
    return norm(lp(c, 5000), 0.95)

@sfx
def seized():
    t = t_(0.7)
    x = signal.sawtooth(2 * np.pi * np.cumsum(400 + 120 * np.sin(2 * np.pi * 11 * t)) / SR) * adsr(0.7, 0.03, 0.2, 0.5, 0.25)
    return norm(bp(x, 300, 2500) * 0.7 + 0.3 * click(0.04, 800, 0.01), 0.5)

@sfx
def valve():
    t = t_(0.6)
    x = signal.sawtooth(2 * np.pi * np.cumsum(220 + 60 * t / 0.6) / SR) * adsr(0.6, 0.03, 0.2, 0.5, 0.2)
    return norm(lp(x, 1400) * 0.5 + 0.4 * bp(noise(0.6), 800, 3000) * adsr(0.6, 0.03, 0.2, 0.4, 0.2), 0.45)

@sfx
def oil_flow():
    t = t_(2.2)
    x = bp(noise(2.2), 200, 1400) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)) * adsr(2.2, 0.4, 0.3, 0.6, 0.8)
    return norm(x + 0.2 * lp(noise(2.2), 200), 0.5)

@sfx
def steps():
    c = canvas(1.4)
    for k in range(4):
        at(c, lp(noise(0.12), 600) * env(0.12, 0.002, 0.03) + 0.5 * sweep(120, 70, 0.1) * env(0.1, 0.002, 0.04), 0.33 * k, 0.9)
    return norm(c, 0.6)

@sfx
def watch_wind():
    c = canvas(1.3)
    for k in range(14):
        at(c, click(0.02, 3500, 0.004) + 0.3 * sine(2200, 0.02) * env(0.02, 0.0005, 0.004), 0.08 * k, 0.6 + 0.02 * k)
    at(c, bell(1900, 0.6, 0.2) * 0.35, 1.1)
    return norm(c, 0.55)

@sfx
def watch_tick():
    c = canvas(0.5)
    at(c, click(0.02, 4000, 0.003) + 0.4 * sine(1800, 0.02) * env(0.02, 0.0005, 0.004), 0.0)
    at(c, click(0.02, 3000, 0.003) * 0.7, 0.25)
    return norm(c, 0.6)

@sfx
def prism():
    return norm(bell(2637, 0.5, 0.16, parts=((1, 1), (2.3, 0.4))) * 0.6 + click(0.015, 5000), 0.5)

@sfx
def prism_ok():
    c = canvas(2.0)
    for k, f in enumerate((523, 659, 784, 1047)):
        at(c, bell(f, 1.8, 0.9), 0.12 * k, 0.6)
    return norm(reverb(c, 0.4, 1.2), 0.6)

@sfx
def lamp_light():
    c = canvas(3.5)
    at(c, lp(noise(3.5), 2500) * adsr(3.5, 0.9, 0.5, 0.5, 1.2), 0.0, 0.5)
    at(c, 0.3 * sine(65, 3.5) * adsr(3.5, 0.8, 0.5, 0.6, 1.2), 0.0)
    for k, f in enumerate((392, 494, 587, 784)):
        at(c, bell(f, 2.6, 1.2) * 0.4, 1.0 + 0.3 * k)
    return norm(reverb(c, 0.3, 1.4), 0.7)

@sfx
def cross():
    x = bp(noise(1.4), 300, 3500) * adsr(1.4, 0.5, 0.2, 0.4, 0.6)
    return norm(reverb(x + 0.3 * sine(220, 1.4) * adsr(1.4, 0.5, 0.2, 0.4, 0.6), 0.4, 1.0), 0.4)

@sfx
def ash():
    return norm(bp(noise(0.8), 800, 4000) * adsr(0.8, 0.1, 0.2, 0.4, 0.4), 0.35)

@sfx
def punch():
    c = canvas(0.3)
    at(c, click(0.03, 3500) + 0.7 * sine(520, 0.1) * env(0.1, 0.001, 0.03), 0.0)
    at(c, bell(3000, 0.2, 0.05) * 0.3, 0.01)
    return norm(c, 0.7)

@sfx
def ripple():
    c = canvas(4.0)
    for k in range(12):
        at(c, bell(900 + 70 * k, 1.2, 0.35, parts=((1, 1), (2.01, 0.3))) * 0.3, 0.3 * k)
    at(c, bp(noise(4.0), 400, 3000) * adsr(4.0, 1.0, 0.3, 0.4, 1.5), 0.0, 0.25)
    return norm(reverb(c, 0.4, 1.4), 0.5)

@sfx
def ferry_horn():
    t = t_(2.2)
    x = 0.6 * sine(98, 2.2) + 0.4 * sine(147, 2.2) + 0.25 * sine(196, 2.2)
    return norm(reverb(lp(x, 1200) * adsr(2.2, 0.15, 0.1, 0.9, 0.9), 0.3, 1.4), 0.6)

# a few extra interface / ambience one-shots (the design asks for about eighty effects in six families)
@sfx
def ui_open():
    return norm(bp(noise(0.25), 400, 3000) * adsr(0.25, 0.08, 0.1, 0.4, 0.1) + 0.3 * pluck(520, 0.25, 0.1), 0.35)

@sfx
def ui_close():
    return norm(bp(noise(0.25), 300, 2000) * adsr(0.25, 0.02, 0.1, 0.3, 0.15) + 0.3 * pluck(390, 0.25, 0.1), 0.35)

@sfx
def drip():
    return norm(sweep(2400, 1500, 0.08) * env(0.08, 0.001, 0.025) + 0.3 * bell(1800, 0.3, 0.08), 0.4)

@sfx
def creak():
    t = t_(0.9)
    x = signal.sawtooth(2 * np.pi * np.cumsum(95 + 25 * np.sin(2 * np.pi * 6 * t) + 30 * t) / SR) * adsr(0.9, 0.1, 0.2, 0.5, 0.3)
    return norm(lp(x, 800), 0.4)

@sfx
def thunder():
    return norm(lp(noise(2.5), 250) * adsr(2.5, 0.05, 0.4, 0.5, 1.4) * (1 + 0.5 * np.sin(2 * np.pi * 3 * t_(2.5))), 0.7)

@sfx
def wind_gust():
    return norm(bp(noise(2.0), 150, 1200) * adsr(2.0, 0.8, 0.2, 0.5, 0.8), 0.4)

@sfx
def gull():
    c = canvas(0.8)
    for k, (f0, f1) in enumerate(((1100, 1700), (1500, 1000))):
        at(c, sweep(f0, f1, 0.28) * adsr(0.28, 0.05, 0.1, 0.8, 0.1), 0.3 * k, 0.5)
    return norm(c, 0.4)

@sfx
def paper_slide():
    return norm(bp(noise(0.5), 1000, 6000) * adsr(0.5, 0.1, 0.1, 0.5, 0.25) * 0.5, 0.35)

# ----------------------------------------------------------------- ambience
AMB = {}
def amb(fn):
    AMB[fn.__name__.lstrip("_")] = fn
    return fn

LOOP = 14.0
XF = 1.5

def _lfo(f, sec, depth=0.5, ph=0.0):
    return 1 - depth + depth * (0.5 + 0.5 * np.sin(2 * np.pi * f * t_(sec) + ph))

def _events(sec, rate, make, gain=1.0):
    c = canvas(sec)
    t = 0.5
    while t < sec - 1:
        at(c, make(), t, gain * RNG.uniform(0.5, 1.0))
        t += RNG.exponential(1.0 / rate)
    return c

@amb
def c1():
    sec = LOOP + XF
    drone = 0.5 * sine(55, sec) + 0.3 * sine(82.4, sec) * _lfo(0.11, sec, 0.4) + 0.15 * sine(110.5, sec) * _lfo(0.07, sec, 0.6)
    hiss = lp(pink(sec), 900) * 0.35 * _lfo(0.09, sec, 0.4, 1.0)
    return norm(loopify(drone * 0.45 + hiss, XF), 0.35)

@amb
def c2():
    sec = LOOP + XF
    lap = lp(noise(sec), 500) * _lfo(0.23, sec, 0.55) * 0.5
    creaks = _events(sec, 0.3, lambda: creak(), 0.5)
    drips = _events(sec, 0.45, lambda: lp(drip(), 3000), 0.4)
    drips = reverb(drips, 0.4, 1.0)[: N(sec)]
    wood = 0.25 * sine(62, sec) * _lfo(0.07, sec, 0.5)
    return norm(loopify(lap + creaks * 0.8 + drips + wood, XF), 0.4)

@amb
def c3():
    sec = LOOP + XF
    lap = lp(noise(sec), 600) * _lfo(0.19, sec, 0.6) * 0.5
    fog = lp(pink(sec), 280) * 0.9
    sh = bp(noise(sec), 1200, 3000) * _lfo(0.31, sec, 0.8, 2.0) * 0.07
    return norm(loopify(lap + fog + sh, XF), 0.35)

@amb
def c4_now():
    sec = LOOP + XF
    rain = hp(noise(sec), 2200) * 0.12 * (_lfo(0.4, sec, 0.35) + 0.3)
    drops = lp(_events(sec, 7.0, lambda: bp(noise(0.03), 2000, 7000) * env(0.03, 0.001, 0.01), 0.5), 6000)
    wind = lp(noise(sec), 500) * _lfo(0.13, sec, 0.7, 0.5) * 0.45
    return norm(loopify(rain + drops + wind, XF), 0.4)

@amb
def c4_then():
    sec = LOOP + XF
    rain = hp(noise(sec), 1800) * 0.2 * (_lfo(0.5, sec, 0.4) + 0.4)
    wind = lp(noise(sec), 700) * _lfo(0.17, sec, 0.8, 1.0) * 0.8
    rumble = lp(noise(sec), 110) * _lfo(0.09, sec, 0.7) * 1.6
    lamp = hp(noise(sec), 3500) * 0.03
    thunder_ = reverb(_events(sec, 0.12, lambda: thunder(), 0.7), 0.3, 1.0)[: N(sec)]
    return norm(loopify(rain + wind + rumble + lamp + thunder_, XF), 0.45)

@amb
def c5():
    sec = LOOP + XF
    under = lp(pink(sec), 350) * 1.0
    beat = 0.35 * sine(110, sec) * _lfo(0.5, sec, 0.8) + 0.3 * sine(113.5, sec)
    rev = canvas(sec)
    t = 1.0
    while t < sec - 3:
        b = bell(RNG.choice([330, 392, 440, 523]), 2.4, 1.0, parts=((1, 1), (2.01, 0.4)))
        rev = at(rev, lp(b[::-1], 1600), t, 0.25)
        t += RNG.uniform(2.5, 5.0)
    return norm(loopify(under + beat * 0.5 + rev, XF), 0.35)

@amb
def title():
    sec = LOOP + XF
    wind = lp(noise(sec), 450) * _lfo(0.1, sec, 0.8) * 0.5
    lap = lp(noise(sec), 700) * _lfo(0.2, sec, 0.5) * 0.25
    sparkle = reverb(_events(sec, 0.25, lambda: bell(RNG.choice([784, 988, 1175]), 1.4, 0.5) * 0.3), 0.5, 1.6)[: N(sec)]
    return norm(loopify(wind + lap + sparkle, XF), 0.35)

# -------------------------------------------------------------------- music
MUS = {}
def mus(fn):
    MUS[fn.__name__.lstrip("_")] = fn
    return fn

def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12.0)

D4, E4, F4, G4, A4, B4, C5, D5, E5 = 62, 64, 65, 67, 69, 71, 72, 74, 76
D3, A3 = 50, 57

def musicbox(f, sec=2.2, gain=1.0):
    parts = ((1, 1.0), (2.0, 0.35), (3.0, 0.18), (5.4, 0.12), (7.9, 0.06))
    x = np.zeros(N(sec))
    for k, g in parts:
        x += g * np.sin(2 * np.pi * f * k * t_(sec)) * env(sec, 0.002, 0.9 / (0.5 + 0.5 * k))
    return x * gain

def play(notes, bpm=72, beat=0.5, sec=40.0, gain=1.0, octave=0):
    c = canvas(sec)
    t = 0.0
    for n, ln in notes:
        if n is not None:
            at(c, musicbox(hz(n + 12 * octave), 2.4), t, gain)
        t += ln * 60.0 / bpm
    return c

MOTIF_A = [(D4, 1), (F4, 1), (A4, 1), (G4, 1), (F4, 1), (E4, 1), (D4, 2), (None, 2)]
MOTIF_B = [(E4, 1), (G4, 1), (B4, 1), (A4, 1), (G4, 1), (F4, 1), (E4, 2), (None, 2)]
MOTIF_C = [(F4, 1), (A4, 1), (D5, 1), (C5, 1), (A4, 1), (G4, 1), (F4, 2), (None, 2)]
FULL = MOTIF_A + MOTIF_B + MOTIF_C + MOTIF_A

@mus
def still_water():
    """fragments only: three notes, never completed (title and the last chapter)"""
    c = canvas(48.0)
    t = 0.0
    seq = [(D4, 3.0), (F4, 3.0), (A4, 9.0), (None, 3.0), (G4, 3.0), (F4, 9.0), (None, 3.0)]
    for n, ln in seq:
        if n is not None:
            at(c, musicbox(hz(n), 3.0), t, 0.8)
        t += ln
    at(c, musicbox(hz(D3), 6.0, 0.35), 0.0)
    at(c, musicbox(hz(A3), 6.0, 0.25), 24.0)
    return norm(loopify(reverb(c, 0.45, 2.2)[: N(48.0)], 2.0), 0.55)

@mus
def memory():
    c = canvas(40.0)
    for k, (n, t0) in enumerate(((D4, 1.0), (F4, 5.0), (A4, 9.5), (E4, 16.0), (G4, 20.0), (D4, 26.0), (F4, 30.5))):
        at(c, musicbox(hz(n), 3.2), t0, 0.7)
    at(c, musicbox(hz(D3), 8.0, 0.3), 0.0)
    return norm(reverb(c, 0.5, 2.4)[: N(40.0)], 0.5)

def _complete():
    c = play(FULL, bpm=66, sec=62.0, gain=0.9)
    bass = canvas(62.0)
    for k, (n, t0) in enumerate(((D3, 0.0), (D3 + 5, 7.3), (D3 + 7, 14.5), (D3, 21.8), (D3 + 2, 29.1))):
        at(bass, musicbox(hz(n), 6.0, 0.35), t0)
    return c + bass

@mus
def ending_A():
    return norm(reverb(_complete(), 0.4, 2.0)[: N(60.0)], 0.6)

@mus
def ending_C():
    c = _complete()
    # a second voice a sixth above, and a far bell beneath it
    c2 = play(FULL, bpm=66, sec=62.0, gain=0.3, octave=1)
    c2 = np.pad(c2, (N(0.33), 0))[: len(c)]
    bells = canvas(62.0)
    for t0 in (0.0, 15.0, 30.0, 45.0):
        at(bells, bell(392, 5.0, 2.5, parts=((1, 1), (2.01, 0.4))), t0, 0.25)
    return norm(reverb(c + c2 + bells, 0.45, 2.2)[: N(60.0)], 0.6)

@mus
def ending_B():
    """the motif, played backwards"""
    x = reverb(_complete(), 0.4, 2.0)[: N(60.0)]
    return norm(x[::-1], 0.55)

# --------------------------------------------------------------------- output
def write(kind, name, data):
    d = os.path.join(ROOT, kind)
    os.makedirs(d, exist_ok=True)
    data = np.clip(data, -1, 1).astype(np.float32)
    path = os.path.join(d, name + ".ogg")
    sf.write(path, data, SR, format="OGG", subtype="VORBIS")
    return os.path.getsize(path)

def main():
    only = set(sys.argv[1:])
    total = 0
    failed = []
    for name, fn in SFX.items():
        if only and name not in only:
            continue
        try:
            x = fade(norm(fn(), 0.9), 0.002, 0.02)
            total += write("sfx", name, x)
        except Exception as e:
            failed.append((name, repr(e)))
    for name, fn in AMB.items():
        if only and name not in only:
            continue
        try:
            total += write("amb", name, fn())
        except Exception as e:
            failed.append((name, repr(e)))
    for name, fn in MUS.items():
        if only and name not in only:
            continue
        try:
            total += write("music", name, fade(fn(), 0.02, 0.5))
        except Exception as e:
            failed.append((name, repr(e)))
    for f in failed:
        print("FAILED", f)
    print(f"{len(SFX)} effects, {len(AMB)} ambience loops, {len(MUS)} music cues; {total / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()
