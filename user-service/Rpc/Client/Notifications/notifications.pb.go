// Code generated by protoc-gen-go. DO NOT EDIT.
// source: notifications.proto

package notifications

import proto "github.com/golang/protobuf/proto"
import fmt "fmt"
import math "math"

import (
	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion2 // please upgrade the proto package

type User struct {
	FcmToken             string   `protobuf:"bytes,1,opt,name=fcmToken,proto3" json:"fcmToken,omitempty"`
	Name                 string   `protobuf:"bytes,2,opt,name=name,proto3" json:"name,omitempty"`
	WhatsappNo           string   `protobuf:"bytes,3,opt,name=whatsappNo,proto3" json:"whatsappNo,omitempty"`
	Email                string   `protobuf:"bytes,4,opt,name=email,proto3" json:"email,omitempty"`
	VerificationCode     string   `protobuf:"bytes,5,opt,name=verificationCode,proto3" json:"verificationCode,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *User) Reset()         { *m = User{} }
func (m *User) String() string { return proto.CompactTextString(m) }
func (*User) ProtoMessage()    {}
func (*User) Descriptor() ([]byte, []int) {
	return fileDescriptor_notifications_cd45fa5e1c85d785, []int{0}
}
func (m *User) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_User.Unmarshal(m, b)
}
func (m *User) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_User.Marshal(b, m, deterministic)
}
func (dst *User) XXX_Merge(src proto.Message) {
	xxx_messageInfo_User.Merge(dst, src)
}
func (m *User) XXX_Size() int {
	return xxx_messageInfo_User.Size(m)
}
func (m *User) XXX_DiscardUnknown() {
	xxx_messageInfo_User.DiscardUnknown(m)
}

var xxx_messageInfo_User proto.InternalMessageInfo

func (m *User) GetFcmToken() string {
	if m != nil {
		return m.FcmToken
	}
	return ""
}

func (m *User) GetName() string {
	if m != nil {
		return m.Name
	}
	return ""
}

func (m *User) GetWhatsappNo() string {
	if m != nil {
		return m.WhatsappNo
	}
	return ""
}

func (m *User) GetEmail() string {
	if m != nil {
		return m.Email
	}
	return ""
}

func (m *User) GetVerificationCode() string {
	if m != nil {
		return m.VerificationCode
	}
	return ""
}

type Empty struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Empty) Reset()         { *m = Empty{} }
func (m *Empty) String() string { return proto.CompactTextString(m) }
func (*Empty) ProtoMessage()    {}
func (*Empty) Descriptor() ([]byte, []int) {
	return fileDescriptor_notifications_cd45fa5e1c85d785, []int{1}
}
func (m *Empty) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Empty.Unmarshal(m, b)
}
func (m *Empty) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Empty.Marshal(b, m, deterministic)
}
func (dst *Empty) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Empty.Merge(dst, src)
}
func (m *Empty) XXX_Size() int {
	return xxx_messageInfo_Empty.Size(m)
}
func (m *Empty) XXX_DiscardUnknown() {
	xxx_messageInfo_Empty.DiscardUnknown(m)
}

var xxx_messageInfo_Empty proto.InternalMessageInfo

func init() {
	proto.RegisterType((*User)(nil), "User")
	proto.RegisterType((*Empty)(nil), "Empty")
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// NotificationServiceClient is the client API for NotificationService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type NotificationServiceClient interface {
	SendUserVerificationCode(ctx context.Context, in *User, opts ...grpc.CallOption) (*Empty, error)
}

type notificationServiceClient struct {
	cc *grpc.ClientConn
}

func NewNotificationServiceClient(cc *grpc.ClientConn) NotificationServiceClient {
	return &notificationServiceClient{cc}
}

func (c *notificationServiceClient) SendUserVerificationCode(ctx context.Context, in *User, opts ...grpc.CallOption) (*Empty, error) {
	out := new(Empty)
	err := c.cc.Invoke(ctx, "/NotificationService/SendUserVerificationCode", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// NotificationServiceServer is the server API for NotificationService service.
type NotificationServiceServer interface {
	SendUserVerificationCode(context.Context, *User) (*Empty, error)
}

func RegisterNotificationServiceServer(s *grpc.Server, srv NotificationServiceServer) {
	s.RegisterService(&_NotificationService_serviceDesc, srv)
}

func _NotificationService_SendUserVerificationCode_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(User)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(NotificationServiceServer).SendUserVerificationCode(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/NotificationService/SendUserVerificationCode",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(NotificationServiceServer).SendUserVerificationCode(ctx, req.(*User))
	}
	return interceptor(ctx, in, info, handler)
}

var _NotificationService_serviceDesc = grpc.ServiceDesc{
	ServiceName: "NotificationService",
	HandlerType: (*NotificationServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SendUserVerificationCode",
			Handler:    _NotificationService_SendUserVerificationCode_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "notifications.proto",
}

// NotificationServiceClientClient is the client API for NotificationServiceClient service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type NotificationServiceClientClient interface {
	SendUserVerificationCode(ctx context.Context, in *User, opts ...grpc.CallOption) (*Empty, error)
}

type notificationServiceClientClient struct {
	cc *grpc.ClientConn
}

func NewNotificationServiceClientClient(cc *grpc.ClientConn) NotificationServiceClientClient {
	return &notificationServiceClientClient{cc}
}

func (c *notificationServiceClientClient) SendUserVerificationCode(ctx context.Context, in *User, opts ...grpc.CallOption) (*Empty, error) {
	out := new(Empty)
	err := c.cc.Invoke(ctx, "/NotificationServiceClient/SendUserVerificationCode", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// NotificationServiceClientServer is the server API for NotificationServiceClient service.
type NotificationServiceClientServer interface {
	SendUserVerificationCode(context.Context, *User) (*Empty, error)
}

func RegisterNotificationServiceClientServer(s *grpc.Server, srv NotificationServiceClientServer) {
	s.RegisterService(&_NotificationServiceClient_serviceDesc, srv)
}

func _NotificationServiceClient_SendUserVerificationCode_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(User)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(NotificationServiceClientServer).SendUserVerificationCode(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/NotificationServiceClient/SendUserVerificationCode",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(NotificationServiceClientServer).SendUserVerificationCode(ctx, req.(*User))
	}
	return interceptor(ctx, in, info, handler)
}

var _NotificationServiceClient_serviceDesc = grpc.ServiceDesc{
	ServiceName: "NotificationServiceClient",
	HandlerType: (*NotificationServiceClientServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "SendUserVerificationCode",
			Handler:    _NotificationServiceClient_SendUserVerificationCode_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "notifications.proto",
}

func init() { proto.RegisterFile("notifications.proto", fileDescriptor_notifications_cd45fa5e1c85d785) }

var fileDescriptor_notifications_cd45fa5e1c85d785 = []byte{
	// 211 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xe2, 0x12, 0xce, 0xcb, 0x2f, 0xc9,
	0x4c, 0xcb, 0x4c, 0x4e, 0x2c, 0xc9, 0xcc, 0xcf, 0x2b, 0xd6, 0x2b, 0x28, 0xca, 0x2f, 0xc9, 0x57,
	0x9a, 0xc1, 0xc8, 0xc5, 0x12, 0x5a, 0x9c, 0x5a, 0x24, 0x24, 0xc5, 0xc5, 0x91, 0x96, 0x9c, 0x1b,
	0x92, 0x9f, 0x9d, 0x9a, 0x27, 0xc1, 0xa8, 0xc0, 0xa8, 0xc1, 0x19, 0x04, 0xe7, 0x0b, 0x09, 0x71,
	0xb1, 0xe4, 0x25, 0xe6, 0xa6, 0x4a, 0x30, 0x81, 0xc5, 0xc1, 0x6c, 0x21, 0x39, 0x2e, 0xae, 0xf2,
	0x8c, 0xc4, 0x92, 0xe2, 0xc4, 0x82, 0x02, 0xbf, 0x7c, 0x09, 0x66, 0xb0, 0x0c, 0x92, 0x88, 0x90,
	0x08, 0x17, 0x6b, 0x6a, 0x6e, 0x62, 0x66, 0x8e, 0x04, 0x0b, 0x58, 0x0a, 0xc2, 0x11, 0xd2, 0xe2,
	0x12, 0x28, 0x4b, 0x2d, 0x82, 0xbb, 0xc2, 0x39, 0x3f, 0x25, 0x55, 0x82, 0x15, 0xac, 0x00, 0x43,
	0x5c, 0x89, 0x9d, 0x8b, 0xd5, 0x35, 0xb7, 0xa0, 0xa4, 0xd2, 0xc8, 0x89, 0x4b, 0xd8, 0x0f, 0xc9,
	0xe9, 0xc1, 0xa9, 0x45, 0x65, 0x99, 0xc9, 0xa9, 0x42, 0xda, 0x5c, 0x12, 0xc1, 0xa9, 0x79, 0x29,
	0x20, 0xd7, 0x87, 0xa1, 0xe9, 0x15, 0x62, 0xd5, 0x03, 0x09, 0x4b, 0xb1, 0xe9, 0x81, 0x4d, 0x50,
	0x62, 0x30, 0xf2, 0xe0, 0x92, 0xc4, 0x62, 0x86, 0x73, 0x4e, 0x66, 0x6a, 0x5e, 0x09, 0x49, 0x26,
	0x25, 0xb1, 0x81, 0x03, 0xce, 0x18, 0x10, 0x00, 0x00, 0xff, 0xff, 0x1c, 0xa0, 0x3d, 0x26, 0x4f,
	0x01, 0x00, 0x00,
}
