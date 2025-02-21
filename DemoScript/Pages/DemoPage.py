from common.web_ui_driver import ElmWith
from common.web_ui_driver import WebBasicPage


class DemoPage(WebBasicPage):
    none_elm = {ElmWith.BIZ_NAME: 'None elm',
                ElmWith.TIMEOUT: 3,
                ElmWith.IGNORE_ERR: True,
                ElmWith.XPATH: '//button[contains(text(), "Click 2")]'}
    Hover_Dropdown = {ElmWith.BIZ_NAME: 'Hover_Dropdown'}
    Text_Input_Field = {ElmWith.BIZ_NAME: 'Text_Input_Field',
                        ElmWith.ID: r'myTextInput', }
    Textarea = {ElmWith.BIZ_NAME: 'Textarea',
                ElmWith.NAME: r'textareaName', }
    PreFilled_Text_Field = {ElmWith.BIZ_NAME: 'PreFilled_Text_Field Input box',
                            ElmWith.NAME: r'preText2', }
    click_me_btn = {ElmWith.BIZ_NAME: 'Click Me btn',
                    ElmWith.XPATH: '//button[contains(text(), "Click Me")]'}
    Placeholder_Text_Field = {ElmWith.BIZ_NAME: 'Placeholder_Text_Field',
                              ElmWith.ID: 'placeholderText'}
    Read_Only_Text_Field = {ElmWith.BIZ_NAME: 'Read_Only_Text_Field',
                            ElmWith.ID: 'readOnlyText'}
    mySlider = {ElmWith.ID: 'mySlider'}
    Select_Dropdown = {ElmWith.XPATH: r'//select[@id="mySelect"]'}
    Image_in_iFrame = {ElmWith.BIZ_NAME: 'Image_in_iFrame',
                       }
    RadioButton_1 = {ElmWith.BIZ_NAME: 'RadioButton_1',
                     ElmWith.ID: 'radioButton1'
                     }
    RadioButton_2 = {ElmWith.BIZ_NAME: 'RadioButton_2',
                     ElmWith.ID: 'radioButton2'
                     }
    CheckBox1 = {ElmWith.BIZ_NAME: 'CheckBox1',
                 ElmWith.ID: 'checkBox1'
                 }
    CheckBox2 = {ElmWith.BIZ_NAME: 'CheckBox2',
                 ElmWith.ID: 'checkBox2'
                 }
    CheckBox3 = {ElmWith.BIZ_NAME: 'CheckBox3',
                 ElmWith.ID: 'checkBox3'
                 }
    CheckBox4 = {ElmWith.BIZ_NAME: 'CheckBox4',
                 ElmWith.ID: 'checkBox4'
                 }
    Pre_Check_Box = {ElmWith.BIZ_NAME: 'Pre_Check_Box',
                     ElmWith.ID: 'checkBox5'
                     }
    CheckBox_in_iFrame = {ElmWith.BIZ_NAME: 'CheckBox_in_iFrame',
                          ElmWith.ID: 'checkBox6'
                          }
    Drag_and_Drop_A = {ElmWith.BIZ_NAME: 'Drag_and_Drop_A',
                       ElmWith.ID: r'drop1'}
    Drag_and_Drop_B = {ElmWith.BIZ_NAME: 'Drag_and_Drop_B',
                       ElmWith.ID: r'drop2'}

    def input_demo_page(self, input_data):
        input_value = f'Wing testing {input_data}'
        self.webdriver(**self.none_elm)
        self.webdriver(**self.Text_Input_Field).send_keys(input_value)
        self.webdriver(**self.Textarea).send_keys(input_value)
        self.webdriver(**self.PreFilled_Text_Field).send_keys(input_value)
        self.webdriver(**self.click_me_btn).click()
        self.webdriver(**self.Placeholder_Text_Field).send_keys(input_value)
        self.webdriver(**self.Read_Only_Text_Field).send_keys(input_value)
        self.webdriver(**self.mySlider).send_keys(10)
        self.webdriver(**self.Select_Dropdown).select(2)
        self.webdriver(**self.Select_Dropdown).select('Set to 50%')
        self.webdriver(**self.RadioButton_1).click()
        self.webdriver(**self.RadioButton_2).click()
        self.webdriver(**self.CheckBox1).click()
        self.webdriver(**self.CheckBox2).click()
        self.webdriver(**self.CheckBox3).click()
        self.webdriver(**self.CheckBox4).click()
        self.webdriver(**self.Pre_Check_Box).click()
        a_elm = self.webdriver(**self.Drag_and_Drop_A)
        b_elm = self.webdriver(**self.Drag_and_Drop_B)
        a_elm.drag_to(b_elm)
        self.webdriver.switch_frame('frameName3')
        self.webdriver(**self.CheckBox_in_iFrame).click()
