# Clash Royale Env

<table>
    <tbody>
        <tr>
            <td>Action Space</td>
            <td>Discrete(2304)</td>
        </tr>
        <tr>
            <td>Observation Shape</td>
            <td>(128, 128, 3)</td>
        </tr>
        <tr>
            <td>Observation High</td>
            <td>255</td>
        </tr>
        <tr>
            <td>Observation Low</td>
            <td>0</td>
        </tr>
        <tr>
            <td>Import</td>
            <td>import clash_royale  <br/>gymnasium.make("clash-royale", render_mode="rgb_array")</td>
        </tr>
    </tbody>
</table>

## Description

Clash Royale as a Gymnasium environment.
Supports Python versions 3.10 and above.

### Installation

```bash
pip install git+https://github.com/MSU-AI/clash-royale-rl.git@0.0.1
```

### Usage

1. Import it to train your RL model

```python
import clash_royale
env = gymnasium.make("clash-royale", render_mode="rgb_array")
```

The package relies on ```import``` side-effects to register the environment
name so, even though the package is never explicitly used, its import is
necessary to access the environment.

2. Some sample code
```python
# WARNING: This code is subject to change and may be OUTDATED!
import clash-royale
import gymnasium
env = gymnasium.make("clash-royale", render_mode="rgb_array")

obs, _ = env.reset()
while True:
    # Next action:
    # (feed the observation to your agent here)
    action = env.action_space.sample()

    # Processing:
    obs, reward, terminated, _, info = env.step(action)
    
    # Checking if the player is still alive
    if terminated:
        break

env.close()
```

## Action Space

Clash Royale has the action space `Discrete(2304)`.

| Variable | Meaning            |
|----------|--------------------|
| x        | Card x-coordinate  |
| y        | Card y-coordinate  |
| z        | Card index in hand |

Corresponding action space index of x * y * z.

## Observation Space

The observation will be the RGB image that is displayed to a human player with
observation space `Box(low=0, high=255, shape=(128, 128, 3), dtype=np.uint8)`.


## Version History

- v0.0.1: initial version release with mock api calls for internal testing
