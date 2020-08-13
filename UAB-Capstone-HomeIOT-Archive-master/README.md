# HomeIOT

HomeIOT is a application suite used to control your homes devices, as well as track usage data such as electricity and water usage in real time.

## Live Demo
[https://homeiot.gose.pw](https://homeiot.gose.pw)

## API Docs
[https://api.homeiot.gose.pw](https://api.homeiot.gose.pw)

## Application Archictecture

The application consists of three main components:
- Data Generation [generate.py](backend/generate.py)
  - `generate.py` is solely used to run [generate_functions.py](backend/generate.py), as a singleton class `Generator`. This ensures that we can instantiate the class at any point in the app but not have to reset all device instances. `generate_functions` can be used on its own with `generate.py`, or live with the API.
- Backend REST API (Flask-RESTPlus/SQLAlchemy) found in the subfolder 'backend'
    - The API was designed with API Spec first in mind for documentation.
      - Documentation can be found [https://api.homeiot.gose.pw](https://api.homeiot.gose.pw)
      - Flask-RESTPlus allows defining schema models in-code and allows frontend developers to see the end schema without any functioning backend code to allow for the most efficient workflows
      - A object oriented inheritance model was used in conjuction with the SQLAlchemy Object Resource Management (ORM) layer. For example:
        - All devices implement `Device` ([device.py](backend/dao/device.py)) and using polymorphism, we can identify a Door, Window, or Electric as a device. Even further, a `Light` subclasses `Electric` which further allows us to fine tune what paramaters go with what devices. In this case, not all electric devices will have temperature settings, but `HVAC` does have temperature settings.
      - Using the object oriented models, we created Data Access Objects (DAO's) to allow ease of interfacing the SQL logic for use with the API Views
        - For example, getting graphing data in real time, along with price predictions using sklearn's LinearRegression models was made easy to use anywhere within the app using the usage DAO ([usage.py](backend/dao/usage.py#L174))
      - All historical weather data is obtained from the dark sky API and is preloaded into memory before data generation begins, to ensure speed and limit the number of API calls, as there is a limit.
- Database (PostgreSQL)
  - Hosted on the digitalocean vps instance, UAB database had some issues, not necessarily with the VPN/SSH Tunneling but the actual instance was not consistent
  - Credentials if you need to peek into the db are below:
    - ```
        port: 5432
        user: cs499
        password: 4JCV4amp
        database: cs499
        ip: homeiot.gose.pw
        ```
- Frontend (React/Redux) found in the subfolder 'capstone'
  - [Axios](https://github.com/axios/axios) library was used for all REST API Calls
  - [Material-UI](https://material-ui.com/) was used as the view templating library
  - [React-ApexChart](https://apexcharts.com/docs/react-charts/) was used for dynamic reactive charts
- DevOps related
    - Runs on a DigitalOcean VPS (Ubuntu 19)
    - Backend/Frontend are proxied through Nginx for SSL and vhost handling. Nginx config can be found [HERE](misc_configs/nginx_config)

## Known Bugs/Unimplemented Features
- Dashboard only shows lights, lights are not clickable
- Switch Board only generates live data for electrical devices, not water based devices.