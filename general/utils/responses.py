responses = {
    "UNKNOWN": {
        "status": "failed",
        "status_code": 500,
        "summary": "UNKNOWN",
        "error_code": 10001,
        "english_details": "the server encounter an unknown error.",
        "farsi_details": "خطای نا مشخصی رخ داده است."
    },
    "INVALID_DATA_RECEIVED": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_DATA_RECEIVED",
        "error_code": 1002,
        "english_details": "the data of the request are invalid",
        "farsi_details": "داده های ارسال شده معتبر نیستند."
    },
    "PHONE_NUMBER_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "PHONE_NUMBER_REQUIRED",
        "error_code": 1003,
        "english_details": "phone number field is required.",
        "farsi_details": "وارد کردن شماره تلفن الزامی است."
    },
    "INVALID_PHONE_NUMBER": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_PHONE_NUMBER",
        "error_code": 1004,
        "english_details": "phone number format is invalid.",
        "farsi_details": "فرمت شماره تلفن وارد شده صحیح نمی باشد."
    },
    "PASSWORD_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "PASSWORD_REQUIRED",
        "error_code": 1005,
        "english_details": "password field is required",
        "farsi_details": "وارد کردن کلمه عبور الزامی است."
    },
    "SHORT_LENGTH_PASSWORD": {
        "status": "failed",
        "status_code": 444,
        "summary": "SHORT_LENGTH_PASSWORD",
        "error_code": 1006,
        "english_details": "the password you sent, is too short. password must be contains at least 6 characters",
        "farsi_details": "کلمه عبور وارد شده کوتاه است. کلمه عبور باید حداقل شامل 6 کاراکتر باشد."
    },
    "USER_ALREADY_EXISTS": {
        "status": "failed",
        "status_code": 452,
        "summary": "USER_ALREADY_EXISTS",
        "error_code": 1007,
        "english_details": "user with these information already exists.",
        "farsi_details": "کاربر با مشخصات وارد شده در حال حاضر وجود دارد."
    },
    "USER_CREATED": {
        "status": "success",
        "status_code": 201,
        "summary": "USER_CREATED",
        "error_code": 0,
        "english_details": "user created successfully",
        "farsi_details": "کاربر با موفقیت ثبت شد."
    },
    "OPERATION_DONE": {
        "status": "success",
        "status_code": 200,
        "summary": "OPERATION_DONE",
        "error_code": 0,
        "english_details": "operation done successfully",
        "farsi_details": "عملیات با موفقیت انجام شد."
    },
    "USERNAME_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "USERNAME_REQUIRED",
        "error_code": 1008,
        "english_details": "username field is required.",
        "farsi_details": "واردکردن نام کاربری الزامی است."
    },
    "INVALID_USERNAME": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_USERNAME",
        "error_code": 1009,
        "english_details": "username format is invalid",
        "farsi_details": "فرمت نام کاربری وارد شده صحیح نمی باشد."
    },
    "USER_NOT_EXISTS": {
        "status": "failed",
        "status_code": 404,
        "summary": "USER_NOT_EXISTS",
        "error_code": 1010,
        "english_details": "user with these information does not exists.",
        "farsi_details": "کاربری با اطلاعات وارد شده وجود ندارد."
    },
    "USER_IS_BLOCKED": {
        "status": "failed",
        "status_code": 403,
        "summary": "USER_IS_BLOCKED",
        "error_code": 1011,
        "english_details": "user is blocked.",
        "farsi_details": "کاربر مسدود شده است."
    },
    "EMAIL_SHOULD_BE_VALIDATED": {
        "status": "failed",
        "status_code": 403,
        "summary": "EMAIL_SHOULD_BE_VALIDATED",
        "error_code": 1012,
        "english_details": "email address should be validated.",
        "farsi_details": "آدرس ایمیل باید تایید شود."
    },
    "PHONE_NUMBER_SHOULD_BE_VALIDATED": {
        "status": "failed",
        "status_code": 403,
        "summary": "PHONE_NUMBER_SHOULD_BE_VALIDATED",
        "error_code": 1013,
        "english_details": "phone number should be validated.",
        "farsi_details": "شماره تلفن باید تایید شود."
    },
    "LOGIN_SUCCESSFUL": {
        "status": "success",
        "status_code": 200,
        "summary": "LOGIN_SUCCESSFUL",
        "error_code": 0,
        "english_details": "login was done successfully",
        "farsi_details": "ورود به سیستم با موفقیت انجام شد."
    },
    "REFRESH_TOKEN_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "REFRESH_TOKEN_REQUIRED",
        "error_code": 1014,
        "english_details": "refresh token is required",
        "farsi_details": "وارد کردن رفرشتوکن الزامی است."
    },
    "INVALID_REFRESH_TOKEN": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_REFRESH_TOKEN",
        "error_code": 1015,
        "english_details": "the refresh token format is invalid",
        "farsi_details": "فرمت رفرش توکن وارد شده صحیح نمی باشد."
    },
    "INVALID_OR_EXPIRED_REFRESH_TOKEN": {
        "status": "failed",
        "status_code": 453,
        "summary": "INVALID_OR_EXPIRED_REFRESH_TOKEN",
        "error_code": 1016,
        "english_details": "the refresh token is invalid or expired.",
        "farsi_details": "رفرش توکن وارد شده نا معتبر است و یا منقضی شده است."
    },
    "TOKEN_GENERATED": {
        "status": "success",
        "status_code": 200,
        "summary": "TOKEN_GENERATED",
        "error_code": 0,
        "english_details": "new access and refresh token generated sucessfully",
        "farsi_details": "اکسس و رفرش توکن جدید با موفقیت ایجاد شد."
    },
    "UNAUTHORIZED_ACCESS": {
        "status": "failed",
        "status_code": 401,
        "summary": "UNAUTHORIZED_ACCESS",
        "error_code": 1017,
        "english_details": "authentication failed. you must login first and then access to this resource with right access token.",
        "farsi_details": "احراز هویت انجام نشد. برای دسترسی به این منبع باید ابتدا وارد سیستم شوید."
    },
    "CAN_NOT_SEND_VERIFICATION_CODE": {
        "status": "failed",
        "status_code": 454,
        "summary": "CAN_NOT_SEND_VERIFICATION_CODE",
        "error_code": 1018,
        "english_details": "there is a problem to send verification/entrance code. please try again later.",
        "farsi_details": "مشکلی در ارسال کد تایید/ورود به وجود آمده است. لطفا مجددا اقدام نمایید. "
    },
    "EMAIL_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "EMAIL_REQUIRED",
        "error_code": 1019,
        "english_details": "email field is required.",
        "farsi_details": "وارد کردن آدرس ایمیل الزامی است."
    },
    "INVALID_EMAIL_ADDRESS": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_EMAIL_ADDRESS",
        "error_code": 1020,
        "english_details": "email address format is invalid.",
        "farsi_details": "فرمت آدرس ایمیل وارد شده صحیح نمی باشد."
    },
    "PHONE_NUMBER_OR_EMAIL_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "PHONE_NUMBER_OR_EMAIL_REQUIRED",
        "error_code": 1021,
        "english_details": "phone number or email field is required.",
        "farsi_details": "وارد کردن شماره تلفن یا آدرس ایمیل الزامی است."
    },
    "CODE_TYPE_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "CODE_TYPE_REQUIRED",
        "error_code": 1022,
        "english_details": "code type field is required.",
        "farsi_details": "وارد کردن نوع کد ارسالی الزامی است."
    },
    "INVALID_CODE_TYPE": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_CODE_TYPE",
        "error_code": 1023,
        "english_details": "code type is invalid",
        "farsi_details": "نوع کد ارسالی معتبر نمی باشد."
    },
    "CODE_SENT": {
        "status": "success",
        "status_code": 200,
        "summary": "CODE_SENT",
        "error_code": 0,
        "english_details": "code sent successfully.",
        "farsi_details": "کد موردنظر با موفقیت ارسال شد."
    },
    "PHONE_NUMBER_AND_EMAIL_SHOULD_BE_VALIDATED": {
        "status": "failed",
        "status_code": 403,
        "summary": "PHONE_NUMBER_AND_EMAIL_SHOULD_BE_VALIDATED",
        "error_code": 1024,
        "english_details": "phone number and email should be validated.",
        "farsi_details": "شماره تلفن و آدرس ایمیل باید تایید شوند."
    },
    "VERIFICATION_CODE_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "VERIFICATION_CODE_REQUIRED",
        "error_code": 1025,
        "english_details": "verification code field is required.",
        "farsi_details": "وارد کردن کد تایید الزامی است."
    },
    "INVALID_OR_EXPIRED_VERIFICATION_CODE": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_OR_EXPIRED_VERIFICATION_CODE",
        "error_code": 1026,
        "english_details": "verification code is invalid or expired.",
        "farsi_details": "کد تایید وارد شده معتبر نیست و یا منقضی شده است."
    },
    "CODE_VERIFIED": {
        "status": "success",
        "status_code": 200,
        "summary": "CODE_VERIFIED",
        "error_code": 0,
        "english_details": "code verified successfully.",
        "farsi_details": "کد موردنظر با موفقیت تایید شد."
    },
    "INVALID_NATIONAL_ID": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_NATIONAL_ID",
        "error_code": 1027,
        "english_details": "national id field is invalid.",
        "farsi_details": "کد ملی وارد شده معتبر نمی باشد."
    },
    "USER_UPDATED": {
        "status": "success",
        "status_code": 200,
        "summary": "USER_UPDATED",
        "error_code": 0,
        "english_details": "user information updated successfully.",
        "farsi_details": "اطلاعات کاربر با موفقیت به روزرسانی شد."
    },
    "LOGIN_TYPE_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "LOGIN_TYPE_REQUIRED",
        "error_code": 1028,
        "english_details": "login type field is required.",
        "farsi_details": "وارد کردن نوع ورود الزامی است."
    },
    "INVALID_LOGIN_TYPE": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_LOGIN_TYPE",
        "error_code": 1029,
        "english_details": "login type is invalid.",
        "farsi_details": "نوع ورود تعیین شده معتبر نمی باشد."
    },
    "ENTRANCE_CODE_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "ENTRANCE_CODE_REQUIRED",
        "error_code": 1030,
        "english_details": "entrance code field is required.",
        "farsi_details": "وارد کردن کد ورود الزامی است."
    },
    "INVALID_OR_EXPIRED_ENTRANCE_CODE": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_OR_EXPIRED_ENTRANCE_CODE",
        "error_code": 1031,
        "english_details": "entrance code is invalid or expired.",
        "farsi_details": "کد وارد شده معتبر نیست و یا منقضی شده است."
    },
    "ONE_TIME_PASSWORD_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "ONE_TIME_PASSWORD_REQUIRED",
        "error_code": 1032,
        "english_details": "one-time password field is required.",
        "farsi_details": "واردکردن رمز عبور یکبار مصرف الزامی است."
    },
    "INVALID_OR_EXPIRED_ONE_TIME_PASSWORD": {
        "status": "failed",
        "status_code": 444,
        "summary": "INVALID_OR_EXPIRED_ONE_TIME_PASSWORD",
        "error_code": 1033,
        "english_details": "one-time password is invalid or expired.",
        "farsi_details": "رمز عبور یکبار مصرف وارد شده معتبر نیست و یا منقضی شده است."
    },
    "PASSWORD_RESET": {
        "status": "success",
        "status_code": 200,
        "summary": "PASSWORD_RESET",
        "error_code": 0,
        "english_details": "password reset successfully.",
        "farsi_details": "رمز عبور با موفقیت بازنشانی شد."
    },
    "PHONE_NUMBER_EXISTS": {
        "status": "failed",
        "status_code": 455,
        "summary": "PHONE_NUMBER_EXISTS",
        "error_code": 1034,
        "english_details": "user with this phone number already exists.",
        "farsi_details": "کاربر با شماره تلفن وارد شده در حال حاضر وجود دارد."
    },
    "EMAIL_ADDRESS_EXISTS": {
        "status": "failed",
        "status_code": 456,
        "summary": "EMAIL_ADDRESS_EXISTS",
        "error_code": 1035,
        "english_details": "user with this email already exists.",
        "farsi_details": "کاربر با آدرس ایمیل وارد شده در حال حاضر وجود دارد."
    },
    "USER_ID_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "USER_ID_REQUIRED",
        "error_code": 1014,
        "english_details": "user_id is required",
        "farsi_details": "وارد کردن یوزر ای است."
    },
    "PERMISSION_DENIED": {
        "status": "failed",
        "status_code": 403,
        "summary": "PERMISSION_ERROR",
        "error_code": 1015,
        "english_details": "You don't have permission for this.",
        "farsi_details": "شما دسترسی لازم برای این بخش را ندارید."
    },
    "FIELD_REQUIRED": {
        "status": "failed",
        "status_code": 444,
        "summary": "FIELD ERROR",
        "error_code": 1016,
        "english_details": "please enter required field .",
        "farsi_details": "لطفا فیلد مورد نظر را وارد کنید"
    },
    "USER_DELETED": {
        "status": "success",
        "status_code": 200,
        "summary": "USER_DELETED",
        "error_code": 1016,
        "english_details": "user  deleted successfully.",
        "farsi_details": "کاربر با موفقیت حذف شد."
    },
    "TYPE_CREATED": {
        "status": "success",
        "status_code": 200,
        "summary": "TYPE_CREATED",
        "error_code": 1017,
        "english_details": "type  created successfully.",
        "farsi_details": "تایپ با موفقیت اضافه شد . "
    },
    "TYPE_UPDATED": {
        "status": "success",
        "status_code": 200,
        "summary": "TYPE_UPDATED",
        "error_code": 1018,
        "english_details": "type  updated successfully.",
        "farsi_details": "تایپ با موفقیت به روز رسانی شد . "
    },
    "TYPE_NOT_EXISTS": {
        "status": "failed",
        "status_code": 404,
        "summary": "TYPE_NOT_EXISTS",
        "error_code": 1019,
        "english_details": "type with this id does not exists.",
        "farsi_details": "تاییپ با اطلاعات وارد شده وجود ندارد."
    },
    "TYPE_DELETED": {
        "status": "success",
        "status_code": 200,
        "summary": "TYPE_DELETED",
        "error_code": 1020,
        "english_details": "type  deleted successfully.",
        "farsi_details": "تایپ با موفقیت حذف شد."
    },
    "FILE_ADDED": {
        "status": "success",
        "status_code": 200,
        "summary": "FILE_ADDED",
        "error_code": 1021,
        "english_details": "file  added successfully.",
        "farsi_details": "فایل با موفقیت اضافه شد."
    },
    "FILE_DELETED": {
        "status": "success",
        "status_code": 200,
        "summary": "FILE_DELETED",
        "error_code": 1022,
        "english_details": "file  deleted successfully.",
        "farsi_details": "فایل با موفقیت حذف شد."
    },
    "IMAGE_NOT_EXISTS": {
        "status": "failed",
        "status_code": 404,
        "summary": "IMAGE_NOT_EXISTS",
        "error_code": 1023,
        "english_details": "image with these information does not exists.",
        "farsi_details": "فایلی با اطلاعات وارد شده وجود ندارد."
    },
    "USER_TYPE_ERROR": {
        "status": "failed",
        "status_code": 403,
        "summary": "USER_TYPE_ERROR",
        "error_code": 1024,
        "english_details": "This user does not have the required type to do this .",
        "farsi_details": "این کاربر تایپ لازم برای انجام این کار را ندارد"
    },
    "USER_DONT_SET_TYPE": {
        "status": "failed",
        "status_code": 444,
        "summary": "USER_DONT_SET_TYPE",
        "error_code": 1025,
        "english_details": "Please select a type first.",
        "farsi_details": "لطفا ابتدا یک تایپ انتخاب کنید"
    },
    "PROJECT_CREATED": {
        "status": "success",
        "status_code": 200,
        "summary": "PROJECT_CREATED",
        "error_code": 1026,
        "english_details": "project  created successfully.",
        "farsi_details": "پروژه با موفقیت اضافه شد . "
    },
    "PROJECT_NOT_EXISTS": {
        "status": "failed",
        "status_code": 404,
        "summary": "PROJECT_NOT_EXISTS",
        "error_code": 1027,
        "english_details": "project with these information does not exists.",
        "farsi_details": "پروژه ای با اطلاعات وارد شده وجود ندارد."
    },
    "PROJECT_UPDATED": {
        "status": "success",
        "status_code": 200,
        "summary": "PROJECT_UPDATED",
        "error_code": 1028,
        "english_details": "project  updated successfully.",
        "farsi_details": "پروژه با موفقیت به روز رسانی شد . "
    },
    "PROJECT_DELETED": {
        "status": "success",
        "status_code": 200,
        "summary": "PROJECT_DELETED",
        "error_code": 1029,
        "english_details": "project  deleted successfully.",
        "farsi_details": "پروژه با موفقیت حذف شد."
    },
}
