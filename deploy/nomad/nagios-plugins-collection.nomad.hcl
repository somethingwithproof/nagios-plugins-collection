job "nagios-plugins-collection" {
  datacenters = ["dc1"]
  type = "batch"

  periodic {
    cron             = "*/10 * * * *"
    prohibit_overlap = true
    time_zone        = "UTC"
  }

  group "checks" {
    task "plugin" {
      driver = "docker"
      config {
        image = "ghcr.io/somethingwithproof/nagios-plugins-collection:latest"
        args  = ["--url=https://example.com", "--pattern=Example"]
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
