/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("otcdrti0y3idyxz")

  // remove
  collection.schema.removeField("brbncfnd")

  // remove
  collection.schema.removeField("i0eguxia")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "o2gxigg8",
    "name": "total_students",
    "type": "number",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "noDecimal": false
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "s5dgjtpd",
    "name": "total_classes",
    "type": "number",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "noDecimal": false
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("otcdrti0y3idyxz")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "brbncfnd",
    "name": "total_students",
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
    "id": "i0eguxia",
    "name": "total_classes",
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

  // remove
  collection.schema.removeField("o2gxigg8")

  // remove
  collection.schema.removeField("s5dgjtpd")

  return dao.saveCollection(collection)
})
