# calendar-audit

    $  docker run -p 5432:5432 -v $PWD/db:/var/lib/postgresql/data --env POSTGRES_USER=calendar --env POSTGRES_DB=calendar --env POSTGRES_PASSWORD=calendar --name calendar-db -d postgres

    $ curl -X POST -d "client_id=181815954642-ng6grql3q32fuhfb2gfp19fgdnhvabdd.apps.googleusercontent.com&client_secret=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&backend=google-oauth2&grant_type=password&username=admin@gmail.com&password=admin" http://localhost:8000/auth/token

    $ https://accounts.google.com/o/oauth2/auth?access_type=offline&approval_prompt=auto&client_id=181815954642-ng6grql3q32fuhfb2gfp19fgdnhvabdd.apps.googleusercontent.com&response_type=code&scope=https://www.googleapis.com/auth/calendar.readonly&redirect_uri=http://localhost:3000/login


https://accounts.google.com/o/oauth2/auth
?gsiwebsdk=3
&client_id=181815954642-ng6grql3q32fuhfb2gfp19fgdnhvabdd.apps.googleusercontent.com
&scope=openid%20profile%20email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly
&redirect_uri=storagerelay%3A%2F%2Fhttp%2Flocalhost%3A3000%3Fid%3Dauth285077
&prompt=consent
&access_type=offline
&response_type=code
&include_granted_scopes=true
&enable_serial_consent=true
