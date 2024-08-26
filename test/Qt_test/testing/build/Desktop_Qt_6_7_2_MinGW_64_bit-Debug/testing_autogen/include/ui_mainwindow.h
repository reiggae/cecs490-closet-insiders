/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.7.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QScrollArea>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QLineEdit *lineEdit;
    QPushButton *pushButton;
    QLabel *label;
    QPushButton *pushButton_5;
    QPushButton *pushButton_6;
    QPushButton *pushButton_15;
    QScrollArea *scrollArea;
    QWidget *scrollAreaWidgetContents;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout;
    QPushButton *pushButton_2;
    QMenuBar *menubar;
    QMenu *menuwindow;
    QMenu *menuwindow_2_i_think;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(491, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        lineEdit = new QLineEdit(centralwidget);
        lineEdit->setObjectName("lineEdit");
        lineEdit->setGeometry(QRect(80, 60, 241, 22));
        pushButton = new QPushButton(centralwidget);
        pushButton->setObjectName("pushButton");
        pushButton->setGeometry(QRect(330, 60, 75, 24));
        label = new QLabel(centralwidget);
        label->setObjectName("label");
        label->setGeometry(QRect(180, 10, 121, 31));
        pushButton_5 = new QPushButton(centralwidget);
        pushButton_5->setObjectName("pushButton_5");
        pushButton_5->setGeometry(QRect(10, 10, 51, 51));
        pushButton_6 = new QPushButton(centralwidget);
        pushButton_6->setObjectName("pushButton_6");
        pushButton_6->setGeometry(QRect(430, 10, 51, 51));
        pushButton_15 = new QPushButton(centralwidget);
        pushButton_15->setObjectName("pushButton_15");
        pushButton_15->setGeometry(QRect(30, 490, 431, 51));
        scrollArea = new QScrollArea(centralwidget);
        scrollArea->setObjectName("scrollArea");
        scrollArea->setGeometry(QRect(20, 90, 451, 381));
        scrollArea->setWidgetResizable(true);
        scrollAreaWidgetContents = new QWidget();
        scrollAreaWidgetContents->setObjectName("scrollAreaWidgetContents");
        scrollAreaWidgetContents->setGeometry(QRect(0, 0, 449, 379));
        gridLayoutWidget = new QWidget(scrollAreaWidgetContents);
        gridLayoutWidget->setObjectName("gridLayoutWidget");
        gridLayoutWidget->setGeometry(QRect(10, 10, 431, 361));
        gridLayout = new QGridLayout(gridLayoutWidget);
        gridLayout->setObjectName("gridLayout");
        gridLayout->setContentsMargins(0, 0, 0, 0);
        pushButton_2 = new QPushButton(gridLayoutWidget);
        pushButton_2->setObjectName("pushButton_2");

        gridLayout->addWidget(pushButton_2, 0, 0, 1, 1);

        scrollArea->setWidget(scrollAreaWidgetContents);
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 491, 22));
        menuwindow = new QMenu(menubar);
        menuwindow->setObjectName("menuwindow");
        menuwindow_2_i_think = new QMenu(menubar);
        menuwindow_2_i_think->setObjectName("menuwindow_2_i_think");
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName("statusbar");
        MainWindow->setStatusBar(statusbar);

        menubar->addAction(menuwindow->menuAction());
        menubar->addAction(menuwindow_2_i_think->menuAction());

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        lineEdit->setText(QCoreApplication::translate("MainWindow", "type to search...", nullptr));
        pushButton->setText(QCoreApplication::translate("MainWindow", "Search", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">Inventory</span></p></body></html>", nullptr));
        pushButton_5->setText(QCoreApplication::translate("MainWindow", "Off", nullptr));
        pushButton_6->setText(QCoreApplication::translate("MainWindow", "Settings", nullptr));
        pushButton_15->setText(QCoreApplication::translate("MainWindow", "Outfit Selection", nullptr));
        pushButton_2->setText(QCoreApplication::translate("MainWindow", "PushButton", nullptr));
        menuwindow->setTitle(QCoreApplication::translate("MainWindow", "window", nullptr));
        menuwindow_2_i_think->setTitle(QCoreApplication::translate("MainWindow", "window 2 i think", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
