# byte-builders

A repository made for Foundations of Software Engineering project building.

The chosen language for this project is Python.

Style for this project shall be dictated by PEP 8 - Style Guide for Python Code.

<https://peps.python.org/pep-0008/>

## Setting Up the Database

This application is set up to use a MySQL database. All currently supported distributions of MySQL are compatible. Follow these steps for setup:

1. **Install MySQL**: Make sure you have MySQL installed on your machine. See the following page to learn more about current versions of MySQL and installation instructions: https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/getting-mysql.html

2. **Create Database**: Create a new schema for the application.
    ```bash
    mysql -u root -p -e "CREATE DATABASE trivial_pursuit;"
    ```

3. **Import Schema**: Import the database schema and initial data from the `schema.sql` file in the 'db' folder.
    ```bash
    mysql -u root -p my_database < db/schema.sql
    ```

4. **Verify**: Verify the database setup by checking the contents of the `Questions` table.
    ```bash
    mysql -u root -p -e "USE trivial_pursuit; SELECT * FROM Questions;"
    ```

5. **Create User**: Edit the db/database.env file to create a DB_USER and DB_PASSWORD which will be used to query the database.
    ```bash
    # Load environment variables from .env file
    export $(grep -v '^#' db/database.env | xargs)

    # Check if required variables are set
    if [[ -z "$DB_ROOT_PASSWORD" || -z "$DB_USER" || -z "$DB_PASSWORD" || -z "$DB_NAME" ]]; then
        echo "Required environment variables (DB_ROOT_PASSWORD, DB_USER, DB_PASSWORD, DB_NAME) are not set in .env file."
        exit 1
    fi

    # Create the user
    mysql -u root -p"${DB_ROOT_PASSWORD}" -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"

    # Grant privileges
    mysql -u root -p"${DB_ROOT_PASSWORD}" -e "GRANT SELECT, INSERT ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"

    # Apply the privilege changes
    mysql -u root -p"${DB_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"

    echo "User ${DB_USER} created and granted privileges on ${DB_NAME}."
    ```

## To contribute to the project

- Create an issue that explains the problem you are trying to solve.
- Create a branch where the name describes your issue or change.
- Clone your branch to a local repository.
- Write, add, and commit your changes to your branch.
- Create a pull request into the Master branch with yours as the head.
- There shall be a default reviewer assigned.
- All threads commented on the pull request must be resolved.
- Upon approval, the pull request will be merged.

To learn how to set up an SSH key and clone a git repository
read the following article:

<https://phoenixnap.com/kb/git-clone-ssh>

## Release

To release our project, I have chosen to use the Python module pyinstaller.
There are many benefits to pyinstaller, such as single file install which
make delivering software incredibly clean, and easy.  In addition, you are able
to run the executable without any of the needed modules installed on the target
audiences computer, (even Python!).

To create a release, `cd` into the directory of your project,
and run `pyinstaller -F main.py` this creates a `dist` directory
where the main executable that is created resides.  We then create
a release folder in our main repository, and copy the executable
to this location along with all of the assets required by our project.
Lastly, we zip the folder up, naming it project_name.zip which imagine
will change to the required format for our team project submittal.
This gets stored back into the same folder we just zipped up for ease
of cleaning, and cleanliness of our repo.

A closer look at how `pyinstaller` works can be read about here:

<https://pyinstaller.org/en/stable/>
