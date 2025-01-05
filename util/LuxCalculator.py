import math

from livingLab.util.experiment_constants import  WINDOW_TRANSMITTANCE, ROOM_REFLECTANCE, ROOM_SURFACE_AREA


# static class to calculate lux values
class LuxCalculator:

    @staticmethod
    def calculateLux(lightState, observerX, observerY):

        if lightState.luminance_output == 0:
            return 0

        distance = LuxCalculator.calculateDistance(observerX, observerY, lightState.positionX, lightState.positionY)
        # calculate direct distance
        # inverse square law
        # https://pressbooks.bccampus.ca/lightingforelectricians/chapter/inverse-square-law
        directLux = lightState.luminance_output / (4 * math.pi * distance ** 2)
        indirectLux = (ROOM_REFLECTANCE * lightState.luminance_output) / ROOM_SURFACE_AREA
        return directLux + indirectLux

    @staticmethod
    def calculateLuxAL(lightState, observerX, observerY):

        if lightState.luminance_output == 0:
            return 0

        distance = LuxCalculator.calculateDistance(observerX, observerY, lightState.positionX, lightState.positionY)
        # assume that light source is 1m above the observer
        distance += 1

        # calculate direct distance
        # inverse square law
        # https://pressbooks.bccampus.ca/lightingforelectricians/chapter/inverse-square-law
        directLux = lightState.luminance_output / (4 * math.pi * distance ** 2)
        indirectLux = (ROOM_REFLECTANCE * lightState.luminance_output) / ROOM_SURFACE_AREA
        return directLux + indirectLux

    @staticmethod
    def calculateDistance(observerX, observerY, lightX, lightY):
        return ((observerX - lightX) ** 2 + (observerY - lightY) ** 2) ** 0.5


#  @staticmethod
#  def calculateLuxArtificialLight(lumen, distance):
#      roomHeight = ROOM_HEIGHT_CM
#      heightDifference = roomHeight - sensorHeight
#      return LuxCalculator.calculateLux(lumen, heightDifference, distanceHorizontal)

#    @staticmethod
#    def calculateLuxWindowSimplified(dni, distanceWindow):
#        # https://www.extrica.com/article/21667
#        # 120 lx equals 1 W/m2#
#
#        # inverse square law
#        luxWindow = dni * 120 * WINDOW_TRANSMITTANCE
#        indirectLux = ROOM_REFLECTANCE * luxWindow
#        directLux = luxWindow / (distanceWindow ** 2)
#        return directLux + indirectLux

    @staticmethod
    def calculateWindowLumen(dni):
        # https://www.extrica.com/article/21667
        # 120 lx equals 1 W/m2
        # simplification based on https://anewhouse.com.au/2016/01/window-lighting-levels/#:~:text=Light%20Entering%20The%20Room,will%20be%20around%20900%20lumens.
        return (dni * 120 * WINDOW_TRANSMITTANCE) / (5)
