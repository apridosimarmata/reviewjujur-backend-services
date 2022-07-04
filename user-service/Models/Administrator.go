package Models

import Configs "user-service/Configs"

func GetAdministratorByWhatsApp(administrator *Administrator, whatsappNo string) (err error) {
	if err = Configs.DB.Where("whatsapp_no = ?", whatsappNo).Find(administrator).Error; err != nil {
		return err
	}
	return nil
}

func AdministratorUpdate(administrator *Administrator) (err error) {
	Configs.DB.Save(administrator)
	return nil
}
