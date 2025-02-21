package org.Testing.Web.Pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.pagefactory.AjaxElementLocatorFactory;

public class SeleniumFromPage {

    public WebDriver driver;

    @FindBy(xpath = "//td[contains(text(), \"Textarea\")]/..//textarea[@id=\"myTextarea\"]")
    public WebElement TextareaInputBox;

    @FindBy(id = "readOnlyText")
    public WebElement readOnlyInputBox;

    public SeleniumFromPage(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(new AjaxElementLocatorFactory(driver, 30), this);
    }


}

