job "nagios-plugins-collection" {
  datacenters = ["dc1"]

  group "checks" {
    task "plugin" {
      driver = "docker"
      config {
        image = "ghcr.io/thomasvincent/nagios-plugins-collection:latest"
        args  = ["check_website_status", "--url=https://example.com", "--pattern=Example"]
      }

      env = {
        PYTHONUNBUFFERED = "1"
      }

      resources {
        cpu    = 100
        memory = 128
      }
    }

    # periodic schedule (every 10 minutes)
    periodic {
      cron             = "*/10 * * * *"
      prohibit_overlap = true
      time_zone        = "UTC"
    }
  }
}
