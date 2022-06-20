#include "PeopleDetector.hpp"
#include "processRequest.hpp"


bool hasPeopleFilter(size_t numberOfPeople, bool hasPeople){
    if(hasPeople && numberOfPeople > 0){
        return true;
    }
    else if(!hasPeople && numberOfPeople == 0){
        return true;
    }
    return false;
}

bool minPeopleFilter(size_t numberOfPeople, int minPeople){
    return (numberOfPeople >= minPeople);
}

bool maxPeopleFilter(size_t numberOfPeople, int maxPeople){
    return (numberOfPeople <= maxPeople);
}

bool filterImage(PeopleDetector&& peopleDetector,
                 const std::string& path,
                 bool hasPeople,
                 std::optional<int> minPeople,
                 std::optional<int> maxPeople){
    size_t numberOfPeople = peopleDetector.countPeople(path);

    if(!hasPeopleFilter(numberOfPeople, hasPeople) ||
       minPeople && !minPeopleFilter(numberOfPeople, *minPeople) ||
       maxPeople && !maxPeopleFilter(numberOfPeople, *maxPeople)){
        return false;
    }
    return true;
}

void processRequest(const cv::FileStorage& cascadeFile,
                    const PeopleRequest* request,
                    PeopleResponse* reply){
    std::string path = request->path();
    bool hasPeople = request->has_people();
    std::optional<int> minPeople = request->has_min_people() ?
        std::make_optional(request->min_people()) : std::nullopt;
    std::optional<int> maxPeople = request->has_max_people() ?
        std::make_optional(request->max_people()) : std::nullopt;

    bool result = filterImage(PeopleDetector(cascadeFile.getFirstTopLevelNode()),
                              path, hasPeople, minPeople, maxPeople);

    reply->set_return_value(result);
}
