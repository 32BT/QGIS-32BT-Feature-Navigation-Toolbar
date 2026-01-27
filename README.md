# QGIS-32BT-Feature-Navigation-Toolbar
QGIS plugin for a toolbar to easily navigate a preselected set of features from any featurelayer.

<img width="223" height="41" alt="image" src="https://github.com/user-attachments/assets/693cb433-94ed-4846-9b3c-0212959d7586" />  

### Feature Navigation Toolbar  
**Overview**  
The Feature Navigation Toolbar is meant to quickly browse a prior selection of features. It will select and zoom to each successive feature. It is not much different from the tablebrowser, except that it will also autoselect the current feature. In addition, it has an internal memory which allows it to provide some useful extra functions. It can create samplesets on-the-fly, or reselect the original set. It can also append additional features outside the preselected set, and it will remember and separate between parsed and unparsed features.

Because the browser distinguishes between parsed and unparsed features it can change its browsing behavior so that unparsed features are prioritized. This is especially useful in conjunction with other processing, like labeling features, where you sometimes want to browse back a couple of steps and redo a feature and then recommence where you left off in the unparsed set.

**Installation**  
Use the plugin manager to install the plugin. Alternatively, you can download a zipfile of the code repository using the Code-button available on this repository's github page. In that case, decompress the zipfile into your QGIS plugins directory, or use the plugin management dialog's "Install from ZIP" option. See: https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab  

In the plugin management dialog, make sure the plugin is activated.

<img width="1043" height="488" alt="image" src="https://github.com/user-attachments/assets/07500a0c-4f71-4075-9485-9159576d60fb" /><br/>

#
### Operation  
The menubutton at the left of the toolbar allows you to start a navigation session. Initially, the button will only become available if the active layer in the map legend is a feature layer with at least two or more features selected. 

<img width="215" height="41" alt="image" src="https://github.com/user-attachments/assets/9fec5ca8-6289-4fd6-81fb-24dfe9a53858" /><br/>  
**Load Selection**  
If you click the button, a menu will appear. In the menu you can choose "Load Selection". This will load the current layer selection into the navigator, which in turn will immediately jump to the first feature. 

<img width="244" height="181" alt="image" src="https://github.com/user-attachments/assets/8cbf8879-f955-4a04-8b8a-f63aad26468c" /><br/>

The first feature will now be selected and the view will be zoomed appropriately. The toolbar will show an info label indicating the currently selected item and the total number of items. You can use the navigation buttons to traverse the set of features.  

<img width="216" height="42" alt="image" src="https://github.com/user-attachments/assets/972ca835-1bb6-4d2c-9ab0-a00065359503" /><br/>

#  
As you browse the features one-by-one, you may at some point need to access the selection to, for example, save your work so far, or split the workload. The plugin allows you to select the items already visited, or the items remaining, by choosing the appropriate menuitem. 

**Select All Items**  
This will select all items in the navigator. If you are navigating your original selection, you will have your initial layerselection. If this is a random sample, the selection will be the sampled subset of your original layer selection.

**Select All Preceding Items**  
This will select all items upto, but not including, the current item.  

**Select All Remaining Items**  
This will select all items from the current item and up. It will include the current item.

>[!NOTE]
>You may notice that the infolabel occassionally becomes gray. This indicates that the current item is not part of the active selection in the layer. If you click the navigationbuttons for the next or previous item, the navigator will first reselect and zoom to the current item.
#  
**Random Sample**  
In order to judge the overall quality of a large set of features, it may be useful to sample a random subset of those features. The Random Sample option allows you to quickly generate a subset sample of the initial selectionset. You can choose a subset percentage from the samplemenu or enter a custom subset using the sampledialog. The plugin will randomly select features from the original selection and load it in the navigator. 

<img width="366" height="349" alt="image" src="https://github.com/user-attachments/assets/ea7bbd29-c52d-47ad-8e66-69fdbe3acdae" />
</br>  

If a random subset percentage is active, it will be emphasized in the menu by a **bold** typeface, and the "Clear Sample" option will be available to revert back to the original selectionset.

>[!NOTE]
>The plugin does **not** use any sophisticated geometric logic for the random sample. It merely uses the "random.sample" routine from your current Python environment. This will suffice in most situations. If a more sophisticated sample is desired, apply the desired algorithms to create a selection prior to starting the navigation session.

#  
### Feature Navigation Toolbar API  
**Plugin API**  
The plugin will be available to other plugins through the iface var. If you have a plugin class with iface stored in self._iface, the navigation controller can be found as follows:

```python
navCtl = self._iface.property("32bt.fnt.FeatureNavigationController")
```  

The navigation controller has a method named "selectNextFeature" which can be called after processing a feature. This will trigger the navigation controller to zoom to and select the next feature from the original selection and update the toolbar accordingly. It also stores the current selection in the parsed set of features. Since the plugin may not necessarily be available, your code should look something like this:

```python
def selectNextFeature(self, layer):
    navCtl = self._iface.property("32bt.fnt.FeatureNavigationController")
    if navCtl: navCtl.selectNextFeature(layer)
```

Navigation only works if your layer matches the navigation layer. The current navigation layer can be fetched using the method "activeLayer":

```python
    if navCtl.activeLayer() == layer:
        # layer selection will be updated if you call selectNextFeature
    else:
        # layer selection will be cleared if you call selectNextFeature
```

Removing the selection if the layer does not match, is a "convenience" function for feedbackpurposes. If you prefer to isolate the layer responsibility, you can accomplish the same result with the following example:

```python
def selectNextFeature(self, layer):
    navCtl = self._iface.property("32bt.fnt.FeatureNavigationController")
    if navCtl and navCtl.activeLayer()==layer:
        navCtl.selectNextFeature(layer)
    else:
        layer.removeSelection()
```
