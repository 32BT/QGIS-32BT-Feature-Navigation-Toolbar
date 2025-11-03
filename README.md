# QGIS-Feature-Navigation-Toolbar
QGIS plugin for a toolbar to easily navigate a preselected set of features from any featurelayer.

<img width="223" height="41" alt="image" src="https://github.com/user-attachments/assets/693cb433-94ed-4846-9b3c-0212959d7586" />  

### Feature Navigation Toolbar  
**Overview**  
The Feature Navigation Toolbar is meant to quickly browse a prior selection of features. It will select and zoom to each successive feature. It is not much different from the tablebrowser, except that it will also autoselect the current feature. In addition, it has an internal memory which allows it to provide two important extra functions. It can append additional features outside the preselected set, and it will remember and separate between parsed and unparsed features.

Because the browser distinguishes between parsed and unparsed features it can change its browsing behavior so that unparsed features are prioritized. Sometimes you want to browse back a couple of steps and redo a feature and then recommence where you left off in the unparsed set.

**Installation**  
You can download a zipfile of the code repository using the Code-button available on this repository's github page. Decompress the zipfile into your QGIS plugins directory. The plugin management dialog can do this for you using the "Install from ZIP" option. See: https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab  
In the plugin management dialog, make sure the plugin is activated.

**Start Navigation**  
The resetbutton at the left of the toolbar allows you to start a navigation session.  

<img width="215" height="41" alt="image" src="https://github.com/user-attachments/assets/9fec5ca8-6289-4fd6-81fb-24dfe9a53858" /><br/>  

The button will be available if the active layer in the map legend is a feature layer with at least two or more features selected. If the reset is validated, the selection will be loaded and the tool will immediately jump to the first feature. The feature will be selected and the view will be zoomed appropriately. Use the navigation buttons to traverse the set of features.  

If only one feature is selected, the start-button will not be available. This is generally the case during navigation and prevents accidentally hitting the restart-button. In addition, if another browsing session is currently active, then a reset will always ask you for confirmation. If you inadvertently selected the resetbutton, or you decide to stick with the current browsing session instead, you can simply select cancel. 

<img width="426" height="177" alt="image" src="https://github.com/user-attachments/assets/2e4f7a23-f1a9-437a-9b5a-69b32ce9a4bd" />
