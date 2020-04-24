import * as React from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import { Overlay, Button, Icon } from "react-native-elements";
import ScoreIndicator from "../Components/ScoreIndicator";
import Color from "../Cons/Color";
import CatalogueList from "../Components/CatalogueList";

export default function Concern(props) {
  const [isVisible, setisVisible] = React.useState(false);
  let catalogue = [];
  let prod = props.prod;
  for (var key in prod) {
    catalogue.push(
      <CatalogueList key={key} {...prod[key]} noDescription={true} />
    );
  }
  return (
    <React.Fragment>
      <Overlay
        isVisible={isVisible}
        windowBackgroundColor="rgba(255, 255, 255, .7)"
        overlayBackgroundColor="rgba(225, 225, 225, .7)"
        width="100%"
        height="auto"
      >
        <ScrollView>
          <View
            style={{
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <View
              style={{
                width: "90%",
                flexDirection: "row",
                justifyContent: "flex-end",
                alignItems: "center",
              }}
            >
              <Button
                icon={<Icon name="highlight-off" size={30} />}
                buttonStyle={{
                  backgroundColor: "transparent",
                }}
                onPress={() => setisVisible(false)}
              />
            </View>

            <View
              style={{
                width: "100%",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              {catalogue}
            </View>
          </View>
        </ScrollView>
      </Overlay>
      <View style={styles.report_component}>
        <View style={styles.issue_container}>
          <Text style={styles.issue_name}>{props.issue}</Text>
          {!props.noRecommendation &&
            !(
              Object.keys(prod).length === 0 && prod.constructor === Object
            ) && (
              <Button
                title="Recommendation"
                type="outline"
                titleStyle={styles.issue_reccom_button_title}
                buttonStyle={styles.issue_reccom_button}
                onPress={() => setisVisible(true)}
              />
            )}
        </View>
      </View>
    </React.Fragment>
  );
}

const styles = StyleSheet.create({
  report_component: {
    width: "90%",
    flex: 1,
  },
  issue_container: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingTop: 10,
    width: "100%",
    marginBottom: 5,
  },
  issue_name: {
    fontSize: 22,
    fontWeight: "bold",
    marginRight: 14,
  },
  issue_reccom_button_title: {
    fontSize: 12,
  },
  issue_reccom_button: {
    padding: 8,
    paddingTop: 4,
    paddingBottom: 4,
    borderRadius: 20,
  },
  issue_min_max: {
    flexDirection: "row",
    width: "80%",
    alignItems: "center",
    justifyContent: "space-between",
  },
  issue_min_max_text: {
    fontWeight: "bold",
    fontSize: 16,
    bottom: 10,
  },
});
