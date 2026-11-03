# Jenkins and GitHub webhook setup

1. Install Jenkins Git, GitHub, Pipeline, and (if needed) Docker Pipeline plugins.
2. Create a Pipeline job configured as Pipeline script from SCM.
3. SCM: Git; repository URL: this repository; branch: `*/develop`; script path: `jenkins/Jenkinsfile`.
4. Enable `GitHub hook trigger for GITScm polling`.
5. Add a GitHub repository webhook: `https://YOUR_JENKINS_HOST/github-webhook/`, content type `application/json`, push events, active.
6. Configure a webhook secret and HTTPS. Ensure network rules permit GitHub to reach the webhook endpoint without exposing Jenkins administration unnecessarily.
7. Push a commit to `develop` and verify a Jenkins build starts.

The Jenkins agent needs Python 3, Docker CLI with daemon access, and (for ECR publishing) AWS CLI and an IAM role/credential with narrowly scoped ECR permissions. Never store AWS keys in this repository.
