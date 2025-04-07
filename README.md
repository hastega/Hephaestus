<a name="readme-top"></a>

<center>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</center>


<br />
<div align="center">
  <a href="https://www.hastega.it/">
    <img src="static/images/logo-hastega-bianco-v.png" alt="Hastega Logo" height="260px">
  </a>

  <h1 align="center">HEPHAESTUS</h1>

  <p align="center">
    A powerful Command Line Interface (CLI) tool designed to streamline development workflows through a flexible plugin architecture.
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a>
            <ul>
                <li><a href="#install-on-a-debian-based-linux-distro">Install on a Debian-based Linux Distro</a></li>
                <li><a href="#install-from-source-code">Install from Source Code</a></li>
                <li><a href="#try-it-in-docker">Try it in Docker</a></li>
                <li><a href="#other-os">Other OS</a></li>
            </ul>
        </li>
      </ul>
    </li>
    <li><a href="#commands">Commands</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

Hephaestus is a versatile CLI tool built to enhance developer productivity. Its core strength lies in its plugin-based architecture, which allows for easy extension and customization. Developers can create and integrate new functionalities as plugins, keeping the core program clean and modular. This approach ensures that Hephaestus can adapt to evolving needs and workflows without requiring extensive code modifications.

### Built With

*   [![Python][Python]][Python]

## Getting Started

### Prerequisites

*   **Python 3.8+:** Hephaestus is built on Python and requires a compatible version.
*   **Git:** Required for installing plugins from Git repositories.
*   **pip:** Python package installer.

### Installation

#### Install on a Debian-based Linux Distro

1.  **Add Google Cloud Keyring:**

    ```shell
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/google-keyring.gpg
    ```

2.  **Add APT Source List:**

    ```shell
    echo 'deb [signed-by=/usr/share/keyrings/google-keyring.gpg] https://europe-west1-apt.pkg.dev/projects/hastega-global-resources hastega main' | sudo tee -a /etc/apt/sources.list.d/hastega.list
    ```

3.  **Update and Install:**

    ```shell
    sudo apt update
    sudo apt install git pip python3-hep
    ```
    **Note:** If you have problems with `sudo` try to run the commands without it.

#### Install from Source Code

1.  **Clone the Repository:**

    ```shell
    git clone https://github.com/hastega/Hephaestus.git
    ```

2.  **Navigate to the Directory:**

    ```shell
    cd Hephaestus
    ```

3.  **Install with pip:**

    ```shell
    pip install .
    ```

    **Note:** In some cases, `pip` might suggest using the `--break-system-packages` parameter. Use it if necessary.

#### Try it in Docker

Quickly test Hephaestus in a disposable Docker container:

```bash
docker run -e TERM -e COLORTERM -w /root -it --rm debian bash -uec '
curl  https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/google-keyring.gpg
echo 'deb [signed-by=/usr/share/keyrings/google-keyring.gpg] https://europe-west1-apt.pkg.dev/projects/hastega-global-resources hastega main' | sudo tee -a  /etc/apt/sources.list.d/artifact-registry.list
sudo apt update
sudo apt install git python3-hep'
```

This command will:

- Run a debian container.
- Install the Hephaestus package.
- Delete the container after exit.


#### Other OS
If you are using another OS, you can try to install it from source code.

## Commands

### RUN

Executes a specified plugin.

#### Syntax

```bash
hep run <plugin_name>
```

### INSTALL

Installs a plugin from a Git repository (HTTPS or SSH).

#### Syntax

```bash
hep install <repository_url>
```

### UNINSTALL

Removes a previously installed plugin.

#### Syntax

```bash
hep uninstall <plugin_name>
```

### LIST

Displays a list of all installed plugins.

#### Syntax

```bash
hep list
```

### UPDATE

Checks for available updates for all or a specific plugin.

#### Syntax

```bash
hep update [<plugin_name>]
```

### UPGRADE

Upgrade all plugins or only the specified one.

#### Syntax

```bash
hep upgrade [<plugin_name>]
```

### NEW PLUGIN

Creates a new plugin project in the current directory based on the default plugin template.

#### Syntax

```bash
hep new-plugin <plugin_name>
```

## Roadmap

### Version 1.0.0 (Released):
- Core plugin management functionality (install, uninstall, list, run).
- Basic update and upgrade capabilities.
- New plugin creation.
### Future Enhancements:
- Comprehensive documentation and tutorials.
- Improved error handling and user feedback.
- Plugin dependency management.

## Contributing
We welcome contributions to Hephaestus! If you're interested in helping out, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and commit them with clear messages.
4. **Submit a pull request** to the main repository.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## Contact

HASTEGA - [HASTEGA](https://www.hastega.it/) - <connect@hastega.it>

David Rainò - [CTO](https://www.linkedin.com/in/david-rain%C3%B2-548084a1/) - <d.raino@hastega.it>

Daniel Angelozzi - [MAINTAINER](https://www.linkedin.com/in/pablo1255/) - <d.angelozzi@hastega.it>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/hastega/Hephaestus?style=for-the-badge
[contributors-url]: https://github.com/hastega/Hephaestus/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/hastega/Hephaestus?style=for-the-badge
[forks-url]: https://github.com/hastega/Hephaestus/network/members
[stars-shield]: https://img.shields.io/github/stars/hastega/Hephaestus?style=for-the-badge
[stars-url]: https://github.com/hastega/Hephaestus/stargazers
[issues-shield]: https://img.shields.io/github/issues/hastega/Hephaestus?style=for-the-badge
[issues-url]: https://github.com/hastega/Hephaestus/issues
[license-shield]: https://img.shields.io/github/license/hastega/Hephaestus?style=for-the-badge
[license-url]: https://github.com/hastega/Hephaestus/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/hastega/
[Python]: https://img.shields.io/badge/-Python-3178C6?logo=python&logoColor=white&style=for-the-badge
[Python-url]: https://www.python.org
