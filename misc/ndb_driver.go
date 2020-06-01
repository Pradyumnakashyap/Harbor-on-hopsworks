package main
import (

  "database/sql"
  _"github.com/go-sql-driver/mysql"
)
func main() {
  db, err := sql.Open("mysql",
"kthfs:<password>@tcp(10.0.2.15:3306)/hopsworks")

 if err != nil {
    panic(err.Error())
  }

  defer db.Close()

  tl, err := db.Query("Show Databases")
        if err != nil {
                panic(err.Error())
  }

type Database struct {

    Name string `json:"name"`
}

  for tl.Next() {

        var database Database

        err = tl.Scan(&database.Name)
        if err != nil {
            panic(err.Error())
        }

        println(database.Name)
}}

