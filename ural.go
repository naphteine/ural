package main

import (
	"database/sql"
	"fmt"
	"html/template"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

const (
	tmplParts   = "templates/parts.html"
	tmplIndex   = "templates/index.html"
	tmplProject = "templates/project.html"
)

// ProjectData holds various columns of project table
type ProjectData struct {
	ID       int
	Name     string
	Idea     string
	Category string
	Language string
	Date     string
}

// IssuesData holds various columns of issues table
type IssuesData struct {
	ID          int
	ProjectID   int
	Description string
	Date        string
	FinishDate  string
	Weight      int
	Type        int
}

var tmpl = make(map[string]*template.Template)

func getDate() string {
	current := time.Now()
	return current.Format("2006-01-02 15:04:05 -0700")
}

func main() {
	// Database
	db, err := sql.Open("sqlite3", "./ural.db")
	if err != nil {
		panic(err)
	}

	// Prepare templates
	tmpl[tmplIndex] = template.Must(template.ParseFiles(tmplIndex, tmplParts))
	tmpl[tmplProject] = template.Must(template.ParseFiles(tmplProject, tmplParts))

	// Router
	r := mux.NewRouter()

	r.HandleFunc("/", func(response http.ResponseWriter, request *http.Request) {
		row, err := db.Query("SELECT id, idea, name FROM projects")
		if err != nil {
			panic(err)
		}
		defer row.Close()

		var projects []ProjectData

		for row.Next() {
			var id int
			var name sql.NullString
			var idea string

			err = row.Scan(&id, &idea, &name)
			if err != nil {
				panic(err)
			}

			projects = append(projects, ProjectData{ID: id, Name: name.String, Idea: idea})
		}

		// Execute template with prepared data
		err = tmpl[tmplIndex].Execute(response, projects)

		if err != nil {
			return
		}
	})

	r.HandleFunc("/project/{id}", func(response http.ResponseWriter, request *http.Request) {
		// Get variables
		vars := mux.Vars(request)
		pid := vars["id"]

		// Set up main data holder
		type ProjectPageData struct {
			Projects []ProjectData
			Issues   []IssuesData
		}

		var projectPageData ProjectPageData

		// Get projects data
		row, err := db.Query("SELECT id, name, idea, category, lang, date FROM projects WHERE id=?", pid)
		if err != nil {
			panic(err)
		}
		defer row.Close()

		for row.Next() {
			var id int
			var name sql.NullString
			var idea string
			var category sql.NullInt32
			var language sql.NullInt32
			var date string

			err = row.Scan(&id, &name, &idea, &category, &language, &date)
			if err != nil {
				panic(err)
			}

			projectPageData.Projects = append(projectPageData.Projects, ProjectData{ID: id, Name: name.String, Idea: idea, Category: strconv.Itoa(int(category.Int32)), Language: strconv.Itoa(int(language.Int32)), Date: date})
		}

		row.Close()

		// Get issues data
		row, err = db.Query("SELECT issue_id, description, date, finish_date, weight, type FROM issues WHERE project_id=?", pid)
		if err != nil {
			panic(err)
		}
		defer row.Close()

		for row.Next() {
			var id int
			var description string
			var date string
			var finishDate sql.NullString
			var weight sql.NullInt32
			var typeOf sql.NullInt32

			err = row.Scan(&id, &description, &date, &finishDate, &weight, &typeOf)
			if err != nil {
				panic(err)
			}

			projectPageData.Issues = append(projectPageData.Issues, IssuesData{ID: id, Description: description, Date: date, FinishDate: finishDate.String, Weight: int(weight.Int32), Type: int(typeOf.Int32)})
		}

		// Execute template with prepared data
		err = tmpl[tmplProject].Execute(response, projectPageData)

		if err != nil {
			return
		}
	})

	r.HandleFunc("/post/project", func(response http.ResponseWriter, request *http.Request) {
		// Check request method
		if request.Method != "POST" {
			http.Redirect(response, request, "/error", 302)
			return
		}

		// Get fields
		name := request.FormValue("name")
		idea := request.FormValue("idea")
		date := getDate()

		// Check if any of the fields are empty
		if idea == "" {
			http.Redirect(response, request, "/error", 302)
			return
		}

		// Add project to database
		if name == "" {
			var err error
			stmt, err := db.Prepare("INSERT INTO projects (idea,date) VALUES ($1,$2)")

			if err != nil {
				http.Redirect(response, request, "/error", 302)
				return
			}

			res, err := stmt.Exec(idea, date)

			if err != nil {
				panic(err)
			}

			affect, err := res.RowsAffected()
			if err != nil {
				panic(err)
			}

			fmt.Println(affect)
		} else {
			var err error
			stmt, err := db.Prepare("INSERT INTO projects (name,idea,date) VALUES ($1,$2,$3)")

			if err != nil {
				http.Redirect(response, request, "/error", 302)
				return
			}

			res, err := stmt.Exec(name, idea, date)

			if err != nil {
				panic(err)
			}

			affect, err := res.RowsAffected()
			if err != nil {
				panic(err)
			}

			fmt.Println(affect)
		}

		// Redirect user
		http.Redirect(response, request, "/", 302)
	})

	r.HandleFunc("/post/issue/{id}", func(response http.ResponseWriter, request *http.Request) {
		// Check request method
		if request.Method != "POST" {
			http.Redirect(response, request, "/error", 302)
			return
		}

		// Get fields
		vars := mux.Vars(request)
		pid := vars["id"]

		issue := request.FormValue("issue")
		typeOf := request.FormValue("type")
		date := getDate()

		// Check if any of the fields are empty
		if issue == "" {
			http.Redirect(response, request, "/error", 302)
			return
		}

		// Add issue to database
		var err error
		stmt, err := db.Prepare("INSERT INTO issues (project_id,description,date,type) VALUES ($1,$2,$3,$4)")

		if err != nil {
			http.Redirect(response, request, "/error", 302)
			return
		}

		res, err := stmt.Exec(pid, issue, date, typeOf)

		if err != nil {
			panic(err)
		}

		affect, err := res.RowsAffected()
		if err != nil {
			panic(err)
		}

		fmt.Println(affect)

		// Redirect user
		http.Redirect(response, request, "/project/"+pid, 302)
	})

	// File server
	r.PathPrefix("/res/").Handler(http.StripPrefix("/res/", http.FileServer(http.Dir("static"))))

	// Server
	http.ListenAndServe(":8080", r)

	// Shutting down
	db.Close()
}
