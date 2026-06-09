/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "rsh3s6bb",
    "name": "face_encoding",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "wtwi0dji",
    "name": "voice_encoding",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  // remove
  collection.schema.removeField("rsh3s6bb")

  // remove
  collection.schema.removeField("wtwi0dji")

  return dao.saveCollection(collection)
})
