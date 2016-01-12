db.express.aggregate(

  // Pipeline
  [
    // Stage 1
    {
      $unwind: "$trace"
    },

    // Stage 2
    {
      $match: {
          $and: [
              {
                  "status": "FINISHED" 
              },
              {
                  "trace.status" : "FINISHED"
              },
              {
                	"trace.time": {
                              $gte: ISODate("2015-12-01T0:0:0+0800"),
                              $lt: ISODate("2016-01-01T0:0:0+0800")
                          }
              },
              { "courier.name": { $regex: "^((?!测试).)*$"} }
          ]
      }
      
    },

    // Stage 3
    {
      $project: {
        _id: 0,
        expr_num: 1,
        status: 1,
        create_time: 1,
        "finish_time": "$trace.time",
        "name": "$courier.name",
        "id": "$courier.id"
      }
    }
  ]

  // Created with 3T MongoChef, the GUI for MongoDB - http://3t.io/mongochef

);
