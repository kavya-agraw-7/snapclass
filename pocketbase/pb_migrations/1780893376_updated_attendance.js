/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6rqf12f3z12hxvm")

  collection.listRule = "1=1"
  collection.viewRule = "1=1"

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6rqf12f3z12hxvm")

  collection.listRule = null
  collection.viewRule = null

  return dao.saveCollection(collection)
})
