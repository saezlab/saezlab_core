# Rationale

Our architecture consists of a number of Python packages working together. These packages require some common technical functionalities, such as logging or config handling, which are provided in well established solutions such as the logging module of Python standard library. In the past, we relied on our own implementations instead of the established solutions. In a previous attempt we intended to share these implementations across the packages, and we created the pypath-common package for this. Pypath-common came with minimal changes, it was mostly reorganization of existing code, and aimed for a working—but not optimal and future proof—solution asap. To address this shortcoming, we should migrate to standard solutions. To control these standard solutions in a way tailored to our software ecosystem, we should create a minimal layer on top of them. Below we specify what we expect from this new component.

# Specification

## Config handling

- Discovery and merging of configs in priority order
- Working directory, user, package built-in
- Format: YAML
- Choose an established solution, e.g. https://hydra.cc/docs/intro/, https://omegaconf.readthedocs.io/en/latest/ 
- Propagate config parameters to lower level packages

## Logging

- Registry of “our packages”
- Control of dispatching messages to our log file
- Formatter
- Log traceback

### Core requirements logging
- Plug-and-play logging and session management for Python packages.
- Configuration via a YAML file (user provides a config file, no code changes needed for most settings).
- Automatic logger and session setup with a single initialize(config_path) call.
- Console and file logging enabled by default.
- Log file rotation: When a log file exceeds 10 MB, a new file is created (configurable).
- Timestamped log files: Log files include the date in their filename.
- Log directory is created automatically if it does not exist.
- Logger exclusion: User can specify loggers (e.g., pandas, matplotlib) to suppress or set to a higher log level via config.
- Configurable log format, log level, log directory, app name, max file size, and backup count via YAML.
- Session management: Centralized access to config and logger.
- Demo folder: Example usage and configuration provided.
- Tests folder: For unit tests (structure ready).
- Use DictConfig to pass the logging configuration
- Create one logger for each major component of our apps and software ecosystem
- Also generate Json logs
- Include the time zone in timestamps
- Use a queue handler to make log calls non-blocking and async

Optional/Future Requirements
- Per-application log files: Ability to create a dedicated log file for each application (config-ready, not yet implemented).
- Extensible for more session/config features in the future.

## Session

- Has one logger and one config
- Keeps things together and provides access anywhere in the code


---

## Implementation Steps / Checklist

1. **Config handling: YAML loader and merging**
   - Use OmegaConf or Hydra for config loading.
   - Support merging configs from working dir, user, and package defaults.
   - Expose config as a DictConfig object.

2. **Logger setup: rotation, format, exclusion**
   - Implement logger setup with rotation, timestamped files, and both console and file handlers.
   - Allow exclusion or level control of 3rd-party loggers via config.
   - Make all parameters (format, level, dir, app name, size, backup count) configurable.

3. **Session management: central access**
   - Implement a Session class to hold config and logger.
   - Provide global access and ensure singleton pattern.

4. **Demo and example config**
   - Provide a demo script and YAML config showing all features, including logger exclusion and rotation.

5. **Component loggers and JSON logs**
   - Support one logger per major component.
   - Add optional JSON log output, configurable via YAML.

6. **Time zone in timestamps**
   - Ensure log timestamps include time zone info, configurable via YAML.

7. **Async logging with queue handler**
   - Implement non-blocking, async logging using a queue handler for file and/or console logs.

8. **Per-application log files (future)**
   - Design config and code to allow separate log files per app, but implement later.

9. **Unit tests for all modules**
   - Add tests for config loading, logger setup, and session management in the tests/ folder.

---
