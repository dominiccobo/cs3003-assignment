import subprocess

def main():
    print('Starting research method execution.')
    Git.assert_git_available_on_path()
    Java.assert_java_available_on_path()
    RepositoryAnalyser('git@github.com:jenkinsci/jenkins.git', './metrics').analyse()


class RepositoryAnalyser:

    def __init__(self, repository_url, output_directory) -> None:
        self._repository_url = repository_url
        self._output_directory = output_directory
        self._setup()

    def _setup(self):
        Git.clone(self._repository_url)

    def analyse(self):
        folder = self.get_folder_from_repo_url()
        CodeSmellsAndOOMetricsToolRunner(folder, '{}/code-smells'.format(self._output_directory)).run()

    def get_folder_from_repo_url(self):
        return self._repository_url.split('/')[1].replace('.git', '')


class CodeSmellsAndOOMetricsToolRunner:

    def __init__(self, run_against, output_to) -> None:
        self._output_to = output_to
        self._run_against = run_against
        self._setup()

    @staticmethod
    def _setup():
        Git.clone('git@github.com:tushartushar/DesigniteJava.git')
        Maven.run('-f=./DesigniteJava/pom.xml clean package -DskipTests=true')

    def run(self):
        self._run_code_smells_analysis(self._run_against, self._output_to)

    # noinspection PyMethodMayBeStatic
    def _run_code_smells_analysis(self, input_directory, output_directory):
        app_with_args = './DesigniteJava/target/DesigniteJava.jar -i {} -o {}'.format(input_directory, output_directory)
        Java.run(app_with_args)

    class TypeMetrics:
        FILE_NAME = 'typeMetrics.csv'

    class MethodMetrics:
        FILE_NAME = 'methodMetrics.csv'
        pass

    class ImplementationSmells:
        FILE_NAME = 'implementationCodeSmells.csv'
        pass

    class DesignSmells:
        FILE_NAME = 'designCodeSmells.csv'
        pass


class TestCoverageToolRunner:

    def __init__(self, run_against, output_to) -> None:
        self._output_to = output_to
        self._run_against = run_against
        self._setup()

    @staticmethod
    def _setup():
        pass

    def run(self):
        pass


def run(command):
    command_with_split_args = command.split(' ')
    subprocess.check_call(command_with_split_args)


class Git:

    @staticmethod
    def clone(repository_url):
        command = 'git clone {} --depth=2'.format(repository_url).split(' ')
        subprocess.call(command)

    @staticmethod
    def assert_git_available_on_path():
        print("Checking git is available on the path.")
        try:
            run('git --version')
        except Exception:
            raise Exception("Git not available on path")


class Maven:

    @staticmethod
    def run(maven_args):
        command = 'mvn {}'.format(maven_args).split(' ')
        subprocess.check_call(command)


class Java:

    @staticmethod
    def assert_java_available_on_path():
        print("Checking git is available on the path.")
        try:
            command = 'java -version'.split(' ')
            subprocess.check_call(command)
        except Exception:
            raise Exception("Java not available on path")

    @staticmethod
    def run(application_with_args):
        command = 'java -jar {}'.format(application_with_args)
        run(command)


if __name__ == "__main__":
    main()

