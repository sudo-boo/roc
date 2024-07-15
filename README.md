# roc-swarm

The clip displays two drones coordinating with each other to collect the rewards (which each drone should collect at least once)

<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/af6926fb-df1a-42ae-a53d-7154fac4e0ed" alt="roc-swarm Demo" width="700" height="450">
</p>

---

<be>

**roc-swarm** is a project that explores the coordination between two drones using NEAT (Neuro-Evolution of Augmenting Topologies) for flight control.
The goal is to demonstrate how drones can autonomously collaborate to achieve a common objective in a simulated environment.

I've tried it for two agents, and there is a lot to potentially develop like increasing multiple (both count-wise and type-wise) agents, adding responses to different terrains, etc.

---

### Installation

Clone and install dependencies

```bash
git clone https://github.com/sudo-boo/roc-swarm.git
cd roc-swarm
pip install -r requirements.txt
```
Run the Simulation:

```bash
python roc_swarm_simulation.py
```

### Customization:

Adjust parameters such as drone behavior, environment setup, and simulation duration in `config.ini`.

---

### License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
