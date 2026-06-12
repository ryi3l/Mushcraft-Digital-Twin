# MUSHCRAFT: Digital Twin Project

## Project Overview

This repository contains the Philippine environment simulation logic for an automated white oyster mushroom growing chamber.

**Note:** The scope of this study and simulation is strictly focused on the fruiting stage inside the growing chamber and explicitly excludes the incubation stage.

## Current Simulation State

- **Temperature:** Core temperature drift logic is implemented and stabilizing.
- **Execution Loops:** Refactored to merge real-time and tick-based execution safely.
- **Data Types:** Fixed boolean output bugs by converting specific flags to string data types.

## Upcoming Development

While the core temperature drift logic is now established, the immediate next phase of development focuses on completing the baseline environmental simulation. This involves integrating the remaining active sensor feedback loops to accurately track and calculate the chamber's internal atmosphere.

- **Sensor Simulation**
  - Humidity drift tracking and stabilization loops.
  - CO2 level accumulation and drift.

---

## Future System Architecture

Once the core environmental and sensor simulation program is fully stabilized, the system will be massively expanded to create a fully reactive digital twin. Future iterations will introduce mechanical actuator responses, biological metabolic modeling, and a robust networking back-end.

- **Actuator Control Logic**
  - Intake and exhaust ventilation (Fans).
  - Humidifier regulation.
  - LED lighting cycles.

- **Biological Simulation (Fruiting Stage)**
  - Real-world CO2 emission modeling (calibrated for 600g–800g fruiting bags).
  - Environment-driven growth dynamics and health metrics.

- **Yield Prediction & Classification**
  - Fruiting yield quality grading (Class II – Extra Class).
  - Cap size categorization (Small – Extra Large).
  - Total mass yield estimation (kg).

> **Database & UI Implementation:** Following the completion of the core Python simulation, a centralized database will be implemented for automated, continuous data logging. This database will feed directly into a dedicated web application, featuring a live dashboard for real-time remote monitoring and data visualization of the digital twin.
