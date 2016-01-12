db.third_party_express.aggregate(

  // Pipeline
  [
    // Stage 1
    {
      $unwind: "$express"
    },

    // Stage 2
    {
      $match: { "express.source":"PHH", $and: [ { "create_time": { $gte: ISODate("2015-12-31T00:00:00.000+0800") } } ] }
    },

    // Stage 3
    {
      $project: {"addr": "$express.shipping_address", "district": "$express.district_name", "_id": 0}
    }

  ]

  // Created with 3T MongoChef, the GUI for MongoDB - http://3t.io/mongochef

);
