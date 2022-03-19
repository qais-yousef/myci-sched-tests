def call() {
	script {
		currentBuild.description = "${NODE}: ${DESCRIPTION}"
	}
}
