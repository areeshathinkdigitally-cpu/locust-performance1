pipeline {
  agent any
  options { timestamps() }

  parameters {
    string(name: 'TARGET_HOST', defaultValue: 'https://api-cycle-dev.azurewebsites.net', description: 'Base host only. Example: https://staging-api.yourapp.com')
    choice(name: 'LOCUST_FILE', choices: [
      'weeks/week1_2_basics.py',
      'weeks/week3_4_modular.py',
      'weeks/week5_6_shapes.py',
      'weeks/week7_8_scaling_ci.py'
    ], description: 'Pick week file to demo')
    string(name: 'USERS', defaultValue: '10', description: 'Total users (-u)')
    string(name: 'SPAWN_RATE', defaultValue: '2', description: 'Spawn rate (-r)')
    string(name: 'DURATION', defaultValue: '2m', description: 'Run time (e.g. 2m, 10m)')
    booleanParam(name: 'STRICT_SLA', defaultValue: false, description: 'If true, slow requests become failures (SLA strict)')
    string(name: 'FAIL_RATIO_MAX', defaultValue: '0.01', description: 'Max failure ratio allowed (0.01 = 1%)')
    string(name: 'P95_MAX_MS', defaultValue: '1200', description: 'Max p95 allowed in ms')
  }

  environment {
    VENV_DIR = ".venv"
    REPORT_DIR = "reports"
    LOCUST_FAIL_RATIO_MAX = "${params.FAIL_RATIO_MAX}"
    LOCUST_P95_MAX_MS = "${params.P95_MAX_MS}"
    STRICT_SLA = "${params.STRICT_SLA}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Setup Python + deps') {
      steps {
        script {
          if (isUnix()) {
            sh """
              python3 --version
              python3 -m venv ${VENV_DIR}
              . ${VENV_DIR}/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt
            """
          } else {
            bat """
              python --version
              python -m venv %VENV_DIR%
              call %VENV_DIR%\\Scripts\\activate
              pip install --upgrade pip
              pip install -r requirements.txt
            """
          }
        }
      }
    }

    stage('Run Locust headless + reports') {
      steps {
        script {
          if (isUnix()) {
            sh """
              mkdir -p ${REPORT_DIR}
              . ${VENV_DIR}/bin/activate
              locust -f "${params.LOCUST_FILE}" --headless -u ${params.USERS} -r ${params.SPAWN_RATE} \
                --run-time ${params.DURATION} --host "${params.TARGET_HOST}" \
                --html ${REPORT_DIR}/locust_report.html --csv ${REPORT_DIR}/locust
            """
          } else {
            bat """
              if not exist %REPORT_DIR% mkdir %REPORT_DIR%
              call %VENV_DIR%\\Scripts\\activate
              locust -f "%LOCUST_FILE%" --headless -u %USERS% -r %SPAWN_RATE% ^
                --run-time %DURATION% --host "%TARGET_HOST%" ^
                --html %REPORT_DIR%\\locust_report.html --csv %REPORT_DIR%\\locust
            """
          }
        }
      }
    }

    stage('Quality Gate (p95 + fail ratio)') {
      steps {
        script {
          if (isUnix()) {
            sh """
              . ${VENV_DIR}/bin/activate
              python scripts/check_thresholds.py ${REPORT_DIR}/locust_stats.csv
            """
          } else {
            bat """
              call %VENV_DIR%\\Scripts\\activate
              python scripts\\check_thresholds.py %REPORT_DIR%\\locust_stats.csv
            """
          }
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'reports/**', fingerprint: true
    }
  }
}