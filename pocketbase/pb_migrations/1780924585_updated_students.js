/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  collection.indexes = []

  // remove
  collection.schema.removeField("ygjumxet")

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("xykkotks96yqrhx")

  collection.indexes = [
    "CREATE INDEX `idx_9Cd92aa` ON `students` (`student_id`)"
  ]

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ygjumxet",
    "name": "student_id",
    "type": "text",
    "required": true,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
})
