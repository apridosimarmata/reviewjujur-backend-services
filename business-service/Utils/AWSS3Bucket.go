package Utils

import (
	"bytes"
	"fmt"
	"strings"

	"encoding/base64"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

// TODO fill these in!
const (
	S3_REGION = "us-west-2"
	S3_BUCKET = "sireto"
)

func AddFileToS3(s *session.Session, base64Image string, name string) error {

	i := strings.Index(base64Image, ",")
	dec := base64.NewDecoder(base64.StdEncoding, strings.NewReader(base64Image[i+1:]))
	buf := new(bytes.Buffer)
	buf.ReadFrom(dec)

	_, err := s3.New(s).PutObject(&s3.PutObjectInput{
		Bucket:               aws.String(S3_BUCKET),
		Key:                  aws.String("images/" + name + ".png"),
		ACL:                  aws.String("private"),
		Body:                 bytes.NewReader(buf.Bytes()),
		ContentDisposition:   aws.String("attachment"),
		ServerSideEncryption: aws.String("AES256"),
	})
	fmt.Println(err)
	return err
}
