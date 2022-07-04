package Models

import (
	"math"
	"strconv"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"

	Configs "user-service/Configs"

	"github.com/google/uuid"
)

func (user *User) BeforeCreate(scope *gorm.Scope) error {
	scope.SetColumn("ID", uuid.New().String())
	return nil
}

func Create(user *User) (err error) {
	if err = Configs.DB.Create(user).Error; err != nil {
		return err
	}
	return nil
}

func GetByWhatsappNo(user *User, whatsappNo string) (err error) {
	if err = Configs.DB.Where("whatsapp_no = ?", whatsappNo).Find(user).Error; err != nil {
		return err
	}
	return nil
}

func GetByEmail(user *User, email string) (err error) {
	if err = Configs.DB.Where("email = ?", email).Find(user).Error; err != nil {
		return err
	}
	return nil
}

func GetByUid(user *User, userUid string) (err error) {
	if err = Configs.DB.Where("uuid = ?", userUid).Find(user).Error; err != nil {
		return err
	}
	return nil
}

func Update(user *User) (err error) {
	Configs.DB.Save(user)
	return nil
}

func GetByQuery(users *[]User, query string) (err error) {
	queryLike := "%" + query + "%"

	if err = Configs.DB.Where("name LIKE ? OR phone LIKE ? or email LIKE ?", queryLike, queryLike, queryLike).Find(users).Error; err != nil {
		return err
	}

	return nil
}

func PaginateUser(userPagination UserPagination) (any UserPagination, err error) {
	var res []*User
	Configs.DB.Scopes(paginate(&res, &userPagination, Configs.DB)).Find(&res)

	var usersResponse []UserResponse

	for _, user := range res {
		var userResponse UserResponse
		userResponse.Uuid = user.Uuid.String()
		userResponse.Name = user.Name
		userResponse.Email = user.Email
		userResponse.WhatsappNo = user.WhatsappNo
		userResponse.VerifiedAt = user.VerifiedAt
		if user.UnsuspendAt != nil {
			userResponse.UnsuspendAt = strconv.FormatInt(*user.UnsuspendAt, 10)
		}

		usersResponse = append(usersResponse, userResponse)
	}

	userPagination.Rows = usersResponse

	return userPagination, nil
}

func paginate(value interface{}, userPagination *UserPagination, db *gorm.DB) func(db *gorm.DB) *gorm.DB {
	var totalRows int64
	db.Model(value).Where("name like ? OR email like ? OR whatsapp_no like ?", "%"+userPagination.Query+"%", "%"+userPagination.Query+"%", "%"+userPagination.Query+"%").Count(&totalRows)

	userPagination.TotalRows = totalRows
	userPagination.TotalPages = int(math.Ceil(float64(totalRows) / float64(userPagination.Limit)))

	return func(db *gorm.DB) *gorm.DB {
		return db.Offset(userPagination.GetOffset()).Limit(userPagination.GetLimit()).Order(userPagination.GetSort()).Where("name like ? OR email like ? OR whatsapp_no like ?", "%"+userPagination.Query+"%", "%"+userPagination.Query+"%", "%"+userPagination.Query+"%") //.Where("email like ?", "%"+userPagination.Query+"%").Where("whatsapp_no like ?", "%"+userPagination.Query+"%")
	}
}
