pipeline {
  agent {
    node {
      label 'windows'
    }
  }
  stages {
    stage('SeleniumSiteOpenPage') {
      steps {
        dir('C:\\Users\\user\\PycharmProjects\\SiteSanityCheck\\play_with_python\\SiteSanityCheck') {
            bat 'python SiteOpenPage.py'
      }
    }
    stage('SeleniumSiteSignup') {
      steps {
        dir('C:\\Users\\user\\PycharmProjects\\SiteSanityCheck\\play_with_python\\SiteSanityCheck') {
            bat 'python SiteSignupSanity.py'
      }
    }
  }
}
