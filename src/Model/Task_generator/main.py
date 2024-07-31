import argparse

from Model.Task_generator.task_generator import TaskGenerator


def main() -> None:
    """
    Calls the TaskGenerator.generate_task function, and prints it's output
    """
    args = parse_args()
    print(TaskGenerator.generate_task(int(args.number_of_formulas_in_the_formula_set), args.variables))


def parse_args() -> argparse.ArgumentParser.parse_args:
    """
    Define argument specification and parse arguments for Task generator tool

    Returns:
        Argument namespace
    """
    parser = argparse.ArgumentParser(
        prog='Logic - Task generator',
        description='This tool generates random formula sets, and random consequence formula, creating a logical task.'
    )

    parser.add_argument('-n', '--number_of_formulas_in_the_formula_set', required=True,
                        help='The formula set will contain this number of formulas.')
    parser.add_argument('-v', '--variables', required=True, nargs='+',
                        help="The tool will use this variables, when creating a task. For example: A B C")
    return parser.parse_args()


if __name__ == '__main__':
    main()
