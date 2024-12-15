---
id: 'install-prerequisites'
title: 'Prerequisites'
sidebar_position: 1
slug: '/install/prerequisites'
---

The following are the necessary prerequisites for setting up the DashAR System.

## Hardware Components

To begin building the DashAR System, you will need the following hardware:

- [XREAL AR Glasses](https://www.xreal.com/)
  - For the development of this project, the [XREAL Air2 Pro](https://www.xreal.com/air2) glasses were used.
- [XREAL Beam Pro](https://www.xreal.com/beampro)
  - Since there is no compute on-board the XREAL Air2 Pro Glasses, this device is required. The newer models (XREAL One and XREAL One Pro) have on-board compute.
- [USB-to-OBDII (ELM327) Adapter](https://en.wikipedia.org/wiki/ELM327)
  - This is how the car communicates with the rest of the system.
  - For the development of this project, [this specific adapter](https://www.amazon.com/dp/B0C3B11S7F) was used, for its reliability and stable connectivity. However, any ELM327-based adapter should work (wired or wireless).
- A portable computer
  - For the development of the project, a [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) running [Ubuntu Server 24.04 LTS](https://ubuntu.com/download/raspberry-pi) was used. However, as long as the portable computer selected has the ability to a) run Python, and b) connect to USB-A devices, it should work.

## HUD Application Prerequisites

To build and deploy the HUD application, you must have the following installed on your development system:

- [Unity 3D (2022.03 LTS)](https://unity.com/)
  - [NRSDK (2.3.1)](https://docs.xreal.com/Release%20Note/NRSDK%202.3.1)
  - [Newtonsoft.JSON (3.2.1)](https://docs.unity3d.com/Packages/com.unity.nuget.newtonsoft-json@3.2/manual/index.html)
  - [TextMeshPro](https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.0/manual/index.html)
- [Android Studio](https://developer.android.com/studio)
  - Useful for SDK Version Management.

## Data Aggregator and Server (DAS) Application Prerequisites

To build and deploy the DAS Server, you must have the following installed on your development system:

- [Python 3.12](https://docs.python.org/3/whatsnew/3.12.html)
  - [Tornado Web Server (6.4.2)](https://www.tornadoweb.org/en/stable/)
  - [obd Module (0.7.2)](https://python-obd.readthedocs.io/en/latest/)
