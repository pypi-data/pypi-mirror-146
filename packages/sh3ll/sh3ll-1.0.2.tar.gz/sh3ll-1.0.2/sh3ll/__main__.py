from difflib import SequenceMatcher
from sh3ll.command import command


class IS(object):
    def __init__(self, prefix="CLA>"):
        self.prefix = prefix
        self.commands = []
        self.categories = []
        """
        Param: -variable value
        """

    def run(self):
        while True:
            try:
                line = input(self.prefix).lower()
            except KeyboardInterrupt:
                exit()
            inputted_command = line.split()[0]

            # Parse command into command and arguments
            args = []
            tmp = line.split()[1:]
            count = 0
            for arg in range(len(tmp)):
                if count == 0:
                    if tmp[arg][0] == "'":
                        for arg2 in range(len(tmp[arg + 1:])):
                            if tmp[arg + 1 + arg2][-1] == "'":
                                args.append(''.join([s.strip("'") for s in tmp[arg:arg + arg2 + 2]]))
                                count = len(tmp[arg:arg + arg2 + 1])
                    else:
                        if tmp[arg][-1] != "'":
                            args.append(tmp[arg])
                else:
                    count -= 1

            cmds = [cmd.name for cmd in self.commands]
            catagories = [cmd.category for cmd in self.commands]

            aliases = {}
            for command in self.commands:
                aliases[command.name] = command.aliases

            if inputted_command != "help":
                if inputted_command in cmds and self.commands[cmds.index(inputted_command)].category == "":
                    self.commands[cmds.index(inputted_command)].execute(args)
                elif inputted_command in catagories:
                    if line.split()[1] in cmds:
                        if self.commands[cmds.index(line.split()[1])].category == line.split()[0]:
                            self.commands[cmds.index(line.split()[1])].execute(args[1:])
                    else:
                        for command in self.commands:
                            if line.split()[1] in command.aliases:
                                command.execute(args[1:])
                else:
                    highestSimiliarity = 0
                    mostSimilarCommandId = -1
                    for command in self.commands:
                        similarity = SequenceMatcher(None, command.callName, inputted_command).ratio()
                        if similarity > highestSimiliarity:
                            highestSimiliarity = SequenceMatcher(None, command.callName, inputted_command).ratio()
                            mostSimilarCommandId = command.callName
                    print(f"Command not recognized.\nDid you mean: '{mostSimilarCommandId}'?")
            else:
                self.help()

    def help(self):
        print("help\tDisplays this menu")
        for command in self.commands:
            if command.category == "":
                print(f"{command.name}\t{command.help}")
        print()

        for category in self.categories:
            if category != "":
                print(f"\"{category}\" Commands:\n" + ("-" * (len(category) + 12)))
                cmds = []
                for command in self.commands:
                    if command.category == category:
                        cmds.append(command)

                longest_name = max([len(cmd.name) for cmd in cmds])
                longest_aliases = max([len(str(cmd.aliases)) for cmd in cmds])
                longest_help = max([len(cmd.help) for cmd in cmds])

                print("\tCommand" + (" " * (abs((len(category) + 1 + longest_name) - 7) + 4)) + "Aliases" + (
                            " " * (abs(longest_aliases - 7) + 4)) + "Help" + " " * (abs(longest_help - 4) + 4))
                print("\t" + ("-" * 7) + (" " * (abs((len(category) + 1 + longest_name) - 7) + 4)) + ("-" * 8) + (
                            " " * (abs(longest_aliases - 8) + 4)) + ("-" * 4))

                for command in cmds:
                    if abs(longest_name - len(command.name)) == 0:
                        print(f"\t{category} {command.name}" + (" " * (abs((len(category) + 1 + longest_name) - (
                                    len(category) + len(command.name) + 1)) + 4)), end="")
                    else:
                        print(f"\t{category} {command.name}" + (" " * (
                                    abs((len(category) + 1 + longest_name) - len(f"{category} {command.name}")) + 4)),
                              end="")
                    if abs(longest_aliases - len(str(command.aliases))) == 0:
                        print(f"{command.aliases}    ", end="")
                    else:
                        print(f"{command.aliases}" + (" " * (abs(longest_aliases - len(str(command.aliases))) + 4)),
                              end="")
                    print(f"{command.help}" + (" " * abs(longest_help - len(command.help))))
                print()

    def command(self, name="Unknown command", callName="Uknown command", aliases=[], help="No help given", category=""):
        def wrap(function):
            if category not in self.categories:
                self.categories.append(category)  # Auto register cats
            self.commands.append(
                command(function, name=name, callName=callName, aliases=aliases, help=help, category=category))

            # print(f"[CLA]: Registered command '{name}'")

            def wrapped_function(*args):
                return function(*args)

            return wrapped_function

        return wrap