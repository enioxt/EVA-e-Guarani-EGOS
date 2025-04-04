# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
-

### Changed
- Refactored `subsystems/ETHIK/core/sanitizer.py` to remove redundant module-level logger and rely on injected `KoiosLogger`.
- Refactored `subsystems/ETHIK/core/validator.py` to remove redundant module-level logger and rely on injected `KoiosLogger`.
- Updated `subsystems/CRONOS/service.py` to use `KoiosLogger` for the service itself and correctly handle the logger instantiation for `BackupManager`.

### Deprecated
-

### Removed
- Redundant module-level logger setup in `subsystems/ETHIK/core/sanitizer.py`.
- Redundant module-level logger setup in `subsystems/ETHIK/core/validator.py`.
- Redundant module-level logger setup in `subsystems/NEXUS/core/nexus_core.py`.

### Fixed
- Resolved indentation errors and cleaned up unused code/imports in `subsystems/ETHIK/core/validator.py`.

### Security
-

## [0.1.0] - YYYY-MM-DD

### Added
- Initial project structure setup.
- Basic configuration for subsystems.
