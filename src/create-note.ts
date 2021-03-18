import "reflect-metadata";
import { createConnection } from "typeorm";
import { Note } from "./entity/Note";

createConnection({
    type: "postgres",
    host: "localhost",
    port: 5432,
    username: "postgres",
    password: "pwd",
    database: "moxie",
    entities: [
        Note
    ],
    synchronize: false,
    logging: true
}).then(async connection => {
    // here you can start to work with your entities
    console.log("Inserting a new note into the database...");
    const note = new Note();
    note.title = "First TS title";
    note.content = "and some content";
    await connection.manager.save(note);
    console.log("Saved a new note with id: " + note.id);

    console.log("Loading notes from the database...");
    const notes = await connection.manager.find(Note);
    console.log("Loaded users: ", notes);

    console.log("Here you can setup and run express/koa/any other framework.");
}).catch(error => console.log(error));