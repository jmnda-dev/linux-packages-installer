from rich.table import Table
from app import console, session
from app.cli_options import PrintCommandLineOptions
from app.models import PackagesAndCommands
from app.package_install import PackageInstaller

cli_options = PrintCommandLineOptions()


class ConsoleInputData:
    """
    Performs actions according to the option selected.
    """

    def get_option_1_table_data(self):
        """
        Queries the data of all the packages saved in the database, then create a dictionary with data that will be used in rendering a table.
        returns: class objects represent each row of data in the database
        """
        # query all data
        data_objects = session.query(PackagesAndCommands).all()

        return data_objects

    def package_is_in_db(self, pkg):
        """
        Check if the package exists in the database.
        @param pkg: attribute used to query the package in the database
        @type pkg: string
        @return: package data if exists in database else False
        @rtype: bool
        """
        query = session.query(PackagesAndCommands)
        try:
            package_data = query.filter_by(id=int(pkg))

        # Catch error raised when converting pkg param to int to use as an id in the query fails, meaning pkg param is a
        # package name or slug.
        except ValueError:
            package_data = (
                query.filter_by(package_name=pkg)
                or query.filter_by(slug=pkg)
            )
        if package_data is not None:
            return package_data
        return False

    def validate_console_input(self, console_message=None, value=None, min=1, max=25):
        while True:
            user_input = console.input(console_message)
            if user_input == "":
                console.print(
                    f"[bold]{value} cannot be empty string. Try again[/]",
                    style="#FF4848 on black",
                )
                continue
            elif len(user_input) < min or len(user_input) > max:
                console.print(
                    f"[bold #FF4848]{value} must be between f{min} - {max} characters long. Try again[/]",
                    style="#FF4848 on black",
                )
                continue
            return user_input

    def get_option_2_data(self):
        """
        Runs when option 2 is selected to Collect data from console input.
        @return: A python dictionary containing key/value pair of the package data to save to the database.
        @rtype: dict
        """
        package_name = self.validate_console_input(
            value="package_name",
            console_message="[bold #64C9CF]Enter the name of the Package:[/] \n [bold #64C9CF]>>> [/]",
            min=2,
            max=20,
        )
        package_desc = self.validate_console_input(
            value="package_desc",
            console_message="[bold #64C9CF]Enter a brief description of the Package:[/] \n [bold #64C9CF]>>> [/]",
            min=5,
            max=300,
        )
        slug = self.validate_console_input(
            value="package_name",
            console_message="[bold #64C9CF]Enter the slug to refer the Package:[/] \n [bold #64C9CF]>>> [/]",
            min=2,
            max=30,
        )
        command_debian = self.validate_console_input(
            value="command_debian",
            console_message=f"[bold #64C9CF]Enter the command for installing {package_name} on [i]Debian[/i]:[/] \n [bold #64C9CF]>>> [/]",
            min=2,
            max=1000,
        )
        command_fedora = self.validate_console_input(
            value="command_debian",
            console_message=f"[bold #64C9CF]Enter the command for installing {package_name} on [i]Fedora[/i]:[/] \n [bold #64C9CF]>>> [/]",
            min=2,
            max=1000,
        )
        return {
            "package_name": package_name,
            "package_desc": package_desc,
            "slug": slug,
            "command_debian": command_debian,
            "command_fedora": command_fedora,
        }

    def get_option_3_data(self):
        """
        Runs when option 3 is selected to Collect data from console input.
        @return: A python dictionary containing key/value pair of the package data to save to the database.
        @rtype: dict
        """
        while True:
            pkg_to_query = console.input(
                "Package name, ID or slug \n [bold #64C9CF]>>> [/]"
            )
            package_db_obj = self.package_is_in_db(pkg_to_query)
            if not package_db_obj:
                console.print(
                    f"[bold]{pkg_to_query} could not be found in the database. Try again[/]",
                    style="#FF4848 on black",
                )
                continue
            break
        while True:
            cli_options.print_option_3()
            option = console.input("\nSelect Option [bold #64C9CF]>>> [/]")

            if option == "1":
                return package_db_obj, self.get_option_2_data()

            elif option == "2":
                package_name = self.validate_console_input(
                    value="package_name",
                    console_message="[bold #64C9CF]Enter the name of the Package:[/] \n [bold #64C9CF]>>> [/]",
                    min=2,
                    max=20,
                )
                return package_db_obj, {"package_name": package_name}

            elif option == "3":
                package_desc = self.validate_console_input(
                    value="package_desc",
                    console_message="[bold #64C9CF]Enter a brief description of the Package:[/] \n [bold #64C9CF]>>> [/]",
                    min=5,
                    max=50,
                )
                return package_db_obj, {"package_desc": package_desc}

            elif option == "4":
                slug = self.validate_console_input(
                    value="package_name",
                    console_message="[bold #64C9CF]Enter the slug to refer the Package:[/] \n [bold #64C9CF]>>> [/]",
                    min=2,
                    max=20,
                )
                return package_db_obj, {"slug": slug}

            elif option == "5":
                command_debian = self.validate_console_input(
                    value="command_debian",
                    console_message=f"[bold #64C9CF]Enter the command for installing the package on [i]Debian[/i]:[/] \n [bold #64C9CF]>>> [/]",
                    min=2,
                    max=1000,
                )
                return package_db_obj, {"command_debian": command_debian}

            elif option == "6":
                command_fedora = self.validate_console_input(
                    value="command_debian",
                    console_message=f"[bold #64C9CF]Enter the command for installing the package on [i]Fedora[/i]:[/] \n [bold #64C9CF]>>> [/]",
                    min=2,
                    max=1000,
                )
                return package_db_obj, {"command_fedora": command_fedora}

            elif option == "7":
                break
            else:
                console.print(
                    f"[bold]Invalid option selected. Try again[/]",
                    style="#FF4848 on black",
                )
                continue

    def get_option_4_data(self):
        """
        Runs when option 4 is selected to Collect data from console input.
        @return: class
        @rtype: <class 'PackagesAndCommands'>
        """
        while True:
            pkg_to_query = self.validate_console_input(
                value="package to delete",
                console_message="[bold #64C9CF]Package name, ID or slug:[/] \n [bold #64C9CF]>>> [/]",
            )
            package_db_obj = self.package_is_in_db(pkg_to_query)
            if not package_db_obj:
                console.print(
                    f"[bold]{pkg_to_query} could not be found in the database. Try again[/]",
                    style="#FF4848 on black",
                )
                continue
            return package_db_obj

    def get_option_5_data(self):
        while True:
            linux_sys = self.validate_console_input(
                value="Linux system name",
                console_message="Select the linux distribution.",
            )
            if linux_sys == "1":
                return "debian"
            elif linux_sys == "2":
                return "fedora"
            else:
                console.print(
                    f"[bold]Invalid option. Try again[/]", style="#FF4848 on black"
                )


class CommandOptionActions(ConsoleInputData):
    """
    Execute actions based on option selected
    """

    def create_table(self):
        """Print out a Table of all the Packages saved to the database.

        Args:
            table_data (list): A list containing the data for each package from the database
            for example: table_data =  [
                {
                    "id": 1,
                    "package_name": "VLC",
                    "package_desc": "A media player",
                    "slug": "vlc",
                    "command_debian": ["apt install vlc"],
                    "command_fedora": ["dnf install vlc"]
                }
            ]
        """
        table_data = self.get_option_1_table_data()
        table = Table()

        # Create table Headers. This could be dynamic by getting the database table column names, but will use static
        # values for now.
        table.add_column("ID")
        table.add_column("Package Name")
        table.add_column("Package Description")
        table.add_column("Slug")
        table.add_column("Command Debian")
        table.add_column("Command Fedora")

        for row_data in table_data:
            table.add_row(
                str(
                    row_data.id
                ),  # convert to string to avoid NotRenderableError exception
                row_data.package_name,
                row_data.package_desc,
                row_data.slug,
                row_data.command_debian,
                row_data.command_fedora,
            )
        return table

    def option_1_action(self):
        """
        Print a table of all Packages saved int he database.
        @return: None
        @rtype: None
        """
        table = self.create_table()
        console.print(table)

    def option_2_action(self):
        """
        Saves package data to database
        @return: None
        @rtype: None
        """
        data = self.get_option_2_data()
        pkg_to_add = PackagesAndCommands(**data)
        session.add(pkg_to_add)
        session.commit()

    def option_3_action(self):
        """
        Updates package data to database
        @return: None
        @rtype: None
        """
        package_to_update, data = self.get_option_3_data()
        for field, value in data.items():
            setattr(package_to_update, field, value)
        session.commit()

    def option_4_action(self):
        """
        Deletes package data to database
        @return: None
        @rtype: None
        """
        package_to_delete = self.get_option_4_data()
        package_to_delete.delete()
        session.commit()

    def option_5_action(self, linux_sys):
        """
        Installs packages by calling the install package method
        """
        pkgs_data = session.query(PackagesAndCommands).all()
        for package in pkgs_data:
            pkg_to_install = PackageInstaller(
                pkg_name=package.package_name,
                pkg_slug=package.slug,
                command=package.command_debian
                if linux_sys == "debian"
                else package.command_fedora,
            )
            pkg_to_install.install_package()
            console.print("[reversed] Finished")
