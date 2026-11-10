# SPDX-FileCopyrightText: 2025 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
variable "image" {
  description = "Plugin image; pin a release tag or an @sha256 digest, never latest"
  type        = string
  default     = "ghcr.io/somethingwithproof/nagios-plugins-collection:2.0.1"
}

job "nagios-plugins-collection" {
  datacenters = ["dc1"]
  type        = "batch"

  periodic {
    cron             = "*/10 * * * *"
    prohibit_overlap = true
    time_zone        = "UTC"
  }

  group "checks" {
    # Plugins exit 1-3 for WARNING/CRITICAL/UNKNOWN; rerunning would repeat the
    # check, so a failed run is final until the next periodic launch.
    restart {
      attempts = 0
      mode     = "fail"
    }

    reschedule {
      attempts  = 0
      unlimited = false
    }

    task "plugin" {
      driver = "docker"
      config {
        image = var.image
        # The image has no ENTRYPOINT, so args alone would be executed as the command.
        command = "check_website_status"
        args    = ["--url=https://example.com", "--pattern=Example"]
      }

      env = {
        PYTHONUNBUFFERED = "1"
      }

      resources {
        cpu    = 100
        memory = 128
      }
    }
  }
}
