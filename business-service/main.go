package main

import (
	"business-service/Configs"
	"business-service/Models"
	"business-service/Routes"
	server "business-service/Rpc/Server"

	"fmt"
	"log"
	"net"

	"github.com/jinzhu/gorm"
	"google.golang.org/grpc"
)

func main() {
	var err error
	Configs.DB, err = gorm.Open("mysql", Configs.DbURL(Configs.BuildDBConfig()))
	if err != nil {
		fmt.Println("Status: ", err)
	}

	defer Configs.DB.Close()
	Configs.DB.AutoMigrate(
		&Models.Business{},
		&Models.Province{},
		&Models.Location{},
	)

	s := server.Server{}

	grpcServer := grpc.NewServer()

	go serveGrpc(*grpcServer, s)

	Configs.DB.LogMode(true)

	r := Routes.SetupRouter()

	r.Run(":5002")
}

func serveGrpc(grpcServer grpc.Server, s server.Server) {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", 6002))

	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	server.RegisterBusinessServiceServer(&grpcServer, &s)

	fmt.Println("BUSINESS-SERVICE GRPC: listening on 6002")

	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %s", err)
	}
}
