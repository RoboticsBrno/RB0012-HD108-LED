# HD108 LEDs

We all love addressable LEDs such as WS2812B. But they suffer from two problems:
- they have high current consumption in the off state – about 1 mA.
- It's nice to have a single-wire protocol for driving these LEDs. However
  generating this signal is not often that easy on common microcontrollers.
  Also, there are many flavours out there that differ in the timing
  requirements.
- They have no gamma correction and only 8-bit PWM.

There seem to be a new kind of LED -
[HD108](https://www.rose-lighting.com/wp-content/uploads/sites/53/2022/07/HD108-Specificaion-V1.2.pdf)
that:
- uses traditional SPI,
- has 16-bit PWM + 5-bit brightness control so gamma correction is actually
  possible.
- claims to have 1 µA power consumption when off.

This repository contains PCB & software to test these LEDs.
