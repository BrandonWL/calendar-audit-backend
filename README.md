# calendar-audit

    $  docker run -p 5432:5432 -v $PWD/db:/var/lib/postgresql/data --env POSTGRES_USER=calendar --env POSTGRES_DB=calendar --env POSTGRES_PASSWORD=calendar --name calendar-db -d postgres
